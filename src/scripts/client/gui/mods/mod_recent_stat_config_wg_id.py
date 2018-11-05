# -*- coding: utf-8 -*-
# https://www.apache.org/licenses/LICENSE-2.0.html

from mod_recent_stat_config import Config


class ConfigWgId(Config):
    _defaultConfigPath = "mods/configs/io.github.servb.recent_stat/wg_api_application_id.txt"

    def __init__(self, configPath=_defaultConfigPath):
        # type: (str) -> None
        self._configPath = configPath
        self.wgId = self._defaultWgId()
        self.load()

    @staticmethod
    def _defaultWgId():
        # type: () -> str
        return "6bcfe604e2408e210eb25510a1f6eeaa"

    def load(self):
        # type: () -> None
        try:
            with open(self._configPath, "r") as configFile:
                self.wgId = configFile.readline().strip()
        except IOError:
            self.errorCantFindFile()
