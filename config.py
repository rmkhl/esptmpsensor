# -*- coding: utf-8 -*-
# Copyright © 2022, RMK Haklab ry

import json


_UNCONFIGURED = {"configured": False}


class Config:
    _config = None

    def __init__(self):
        try:
            with open("configuration.json") as fp:
                self._config = json.load(fp)
        except Exception:
            self._config = _UNCONFIGURED.copy()

    def save(self):
        try:
            with open("configuration.json", "w") as fp:
                json.dump(fp)
        except Exception:
            pass  # Not nice but this is a black box nobody is monitoring

    def __getattr__(self, key):
        return self._config.get(key)

    def __setattr__(self, key, value):
        self._config[key] = value
