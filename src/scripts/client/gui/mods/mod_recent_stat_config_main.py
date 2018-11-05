# -*- coding: utf-8 -*-
# https://www.apache.org/licenses/LICENSE-2.0.html

import json

from mod_recent_stat_config import Config
from mod_recent_stat_constant import CONFIG_MAIN
from mod_recent_stat_string import removeComments


class ConfigMain(Config):
    _defaultConfigPath = "mods/configs/io.github.servb.recent_stat/config_main.json"

    _defaultRegion = "ru"
    _defaultTimeout = 10

    def __init__(self, configPath=_defaultConfigPath):
        # type: (str) -> None
        self._configPath = configPath
        self.region = self._defaultRegion
        self.timeout = self._defaultTimeout
        self.load()

    def load(self):
        # type: () -> None
        try:
            with open(self._configPath, "r") as configFile:
                configJson = json.loads(removeComments(configFile.read()))

                if CONFIG_MAIN.REGION in configJson:
                    self.region = configJson[CONFIG_MAIN.REGION]
                else:
                    self.warnNoAttribute(CONFIG_MAIN.REGION)

                if CONFIG_MAIN.TIMEOUT in configJson:
                    self.timeout = configJson[CONFIG_MAIN.TIMEOUT]
                else:
                    self.warnNoAttribute(CONFIG_MAIN.TIMEOUT)
        except IOError:
            self.errorCantFindFile()
