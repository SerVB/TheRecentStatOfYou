# -*- coding: utf-8 -*-
# https://www.apache.org/licenses/LICENSE-2.0.html

from mod_recent_stat_config_format import ConfigFormat
from mod_recent_stat_config_main import ConfigMain
from mod_recent_stat_config_wg_id import ConfigWgId
# from mod_recent_stat_container import updatePlayerFormatByVehicleList, formattedPlayerName
from mod_recent_stat_logging import logInfo
from mod_recent_stat_wg_stats import WgStats


class ModRecentStat:
    def __init__(self, configFormat=None, configMain=None, configWgId=None):
        # type: (ConfigFormat, ConfigMain, ConfigWgId) -> None
        logInfo("Mod loading is started.")

        self._configFormat = configFormat or ConfigFormat()
        self._configMain = configMain or ConfigMain()
        self._configWgId = configWgId or ConfigWgId()

        self._playerIdToData = dict()
        self._wgStats = WgStats(self._configMain, self._configWgId)

        logInfo("Mod loading is finished.")

    def loadPlayerDataByVehicleList(self, vehicles):
        # type: (dict) -> None
        self._wgStats.loadPlayerDataByVehicleList(vehicles, self._playerIdToData)
        # updatePlayerFormatByVehicleList(vehicles)

    def formatPlayerName(self, accountDBID, playerName):
        # type: (int, str) -> str
        playerInfo = self._playerIdToData.get(accountDBID, None)
        if playerInfo is not None:
            newPlayerName = str(playerInfo.xwn8) + " " + str(playerInfo.kb) + "k " + playerName
            # newPlayerName = formattedPlayerName(playerName, configFormat)
            return newPlayerName

        return playerName
