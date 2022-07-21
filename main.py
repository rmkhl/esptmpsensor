# -*- coding: utf-8 -*-
# Copyright © 2022, RMK Haklab ry

from config import Config
from networking import enable_access_point, connect_to_wlan

conf = Config()

if not conf.configured or conf.access_point:
    enable_access_point(conf.wlan_config)
else:
    connect_to_wlan(conf.wlan_config)
