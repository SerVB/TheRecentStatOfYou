# -*- coding: utf-8 -*-
# https://www.apache.org/licenses/LICENSE-2.0.html

from mod_recent_stat_config import Config


class ConfigWgId(Config):
    _defaultConfigPaths = (
        "mods/configs/io.github.servb.recent_stat/wg_api_application_id.txt",
        "../mods/configs/io.github.servb.recent_stat/wg_api_application_id.txt",
    )

    def __init__(self, configPaths=_defaultConfigPaths):
        # type: (tuple) -> None
        self._configPaths = configPaths
        self.wgId = self._defaultWgId()
        self.load()

    @staticmethod
    def _defaultWgId():
        # type: () -> str
        return "6bcfe604e2408e210eb25510a1f6eeaa"

    def load(self):
        # type: () -> None
        anyLoaded = True
        for configPath in self._configPaths:
            try:
                with open(configPath, "r") as configFile:
                    self.wgId = configFile.readline().strip()
            except IOError:
                pass

        if not anyLoaded:
            self.warnCantFindFiles()
