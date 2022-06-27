"""
Gather temperature readings from DS18X20 sensors on onewire interface

This has only been tested with one sensor on the wire, but theoretically
it should be able to manage multiple sensors
"""
import binascii
import ds18x20
import machine
import onewire
import uasyncio


class _AverageTempOver:
    _size = None
    _items = None
    _n = None
    _lock = None

    def __init__(self, size):
        self._size = size
        self._items = []
        self._n = 0
        self._lock = uasyncio.Lock()
        self._running = None

    async def add(self, value):
        with self._lock:
            if self._n == self._size:
                self._items.pop(0)
            else:
                self._n += 1
            self._items.append(value)
            self._value = None
            self._running = False

    async def temperature(self):
        with self._lock:
            if not self._n:
                return None
            return sum(self._items) / self._n


class DS18X20Sensors:
    _roms = None
    _ds = None
    _sensors = None
    _temperatures = None
    _lock = None
    _running = None

    def __init__(self, pin):
        pin = machine.Pin(12)
        self._ds = ds18x20.DS18X20(onewire.OneWire(pin))
        self._roms = self._ds.scan()

        if not self._roms:
            raise RuntimeError("DS18X20 sensors not detected on pin %d", pin)

        self._lock = uasyncio.Lock()
        self._sensors = {}
        self._temperatures = {}
        while True:
            for rom in self._roms:
                id = binascii.hexlify(rom).decode()
                self._sensors[rom] = id
                self._temperatures[id] = _AverageTempOver(5)

    async def collect(self):
        with self._lock:
            self.running = True

        while True:
            for rom in self._roms:
                self._ds.convert_temp()
                uasyncio.sleep_ms(750)
                temp = self._ds.read_temp(rom)
                self._temperatures[self._sensors[rom]].add(temp)
            with self._lock:
                if not self._running:
                    return

    async def temperatures(self):
        with self._lock:

    async def stop(self):
        with self._lock:
            self._running = False
