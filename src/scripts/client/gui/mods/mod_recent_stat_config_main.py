# -*- coding: utf-8 -*-
# https://www.apache.org/licenses/LICENSE-2.0.html

import json

from mod_recent_stat_config import Config
from mod_recent_stat_constant import CONFIG_MAIN, STAT_PROVIDER
from mod_recent_stat_logging import logError
from mod_recent_stat_provider_kttc import Kttc
from mod_recent_stat_provider_noobmeter import Noobmeter
from mod_recent_stat_string import removeComments


class ConfigMain(Config):
    _defaultConfigPath = "mods/configs/io.github.servb.recent_stat/config_main.json"

    _defaultRegion = "ru"
    _defaultTimeout = 10
    _defaultRecentStatProviderName = STAT_PROVIDER.KTTC

    def __init__(self, configPath=_defaultConfigPath):
        # type: (str) -> None
        self._configPath = configPath
        self.region = self._defaultRegion
        self.timeout = self._defaultTimeout
        self.recentStatProvider = None
        self.load()

        self.recentStatProvider = self.recentStatProvider or Kttc()

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

                if CONFIG_MAIN.RECENT_STAT_PROVIDER in configJson:
                    statProvider = configJson[CONFIG_MAIN.RECENT_STAT_PROVIDER]

                    if statProvider not in STAT_PROVIDER.SUPPORTED:
                        self.warnInvalidAttribute(CONFIG_MAIN.RECENT_STAT_PROVIDER, statProvider, STAT_PROVIDER.SUPPORTED)
                    elif statProvider == STAT_PROVIDER.KTTC:
                        self.recentStatProvider = Kttc()
                    elif statProvider == STAT_PROVIDER.NOOBMETER:
                        self.recentStatProvider = Noobmeter()
                    else:
                        logError("Stat provider is supported but not meant by the config initializer: %s" % statProvider, "")
                else:
                    self.warnNoAttribute(CONFIG_MAIN.RECENT_STAT_PROVIDER)
        except IOError:
            self.errorCantFindFile()
