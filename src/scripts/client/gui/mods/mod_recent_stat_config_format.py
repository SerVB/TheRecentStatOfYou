# -*- coding: utf-8 -*-
# https://www.apache.org/licenses/LICENSE-2.0.html

import json

from mod_recent_stat_config import Config
from mod_recent_stat_constant import CONFIG_FORMAT
from mod_recent_stat_string import removeComments


class ConfigFormat(Config):
    _defaultConfigPaths = (
        "mods/configs/io.github.servb.recent_stat/config_format.json",
        "../mods/configs/io.github.servb.recent_stat/config_format.json",
    )

    _defaultPlayerName = "{xwn8} {kb}k "
    _defaultNoInfo = "--"

    def __init__(self, configPaths=_defaultConfigPaths):
        # type: (tuple) -> None
        self._configPaths = configPaths
        self.playerName = self._defaultPlayerName
        self.noInfo = self._defaultNoInfo
        self._load()

    def _load(self):
        # type: () -> None
        anyLoaded = True
        for configPath in self._configPaths:
            try:
                with open(configPath, "r") as configFile:
                    configJson = json.loads(removeComments(configFile.read()))

                    if CONFIG_FORMAT.PLAYER_NAME in configJson:
                        self.playerName = configJson[CONFIG_FORMAT.PLAYER_NAME]
                    else:
                        self.warnNoAttribute(CONFIG_FORMAT.PLAYER_NAME)

                    if CONFIG_FORMAT.NO_INFO in configJson:
                        self.noInfo = configJson[CONFIG_FORMAT.NO_INFO]
                    else:
                        self.warnNoAttribute(CONFIG_FORMAT.NO_INFO)
            except IOError:
                pass

        if not anyLoaded:
            self.warnCantFindFiles()

    def __str__(self):
        # type: () -> str
        return "{playerName='%s', noInfo='%s'}" % (self.playerName, self.noInfo)
