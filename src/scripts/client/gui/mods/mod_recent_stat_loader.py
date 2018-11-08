# -*- coding: utf-8 -*-
# https://www.apache.org/licenses/LICENSE-2.0.html

from threading import Thread
import traceback

from mod_recent_stat_config_format import ConfigFormat
from mod_recent_stat_config_main import ConfigMain
from mod_recent_stat_config_wg_id import ConfigWgId
from mod_recent_stat_logging import logInfo, logError
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

        try:
            vehicleInfoTasks = set()

            for _vehicleID, vehicleData in vehicles.iteritems():
                if "name" in vehicleData and "accountDBID" in vehicleData:
                    playerName = vehicleData["name"]
                    playerId = vehicleData["accountDBID"]

                    if playerId in self._playerIdToData and self._playerIdToData[playerId].hasRecentStat:
                        continue

                    task = Thread(
                        target=self._configMain.recentStatProvider.getStatistics,
                        args=(self._configMain.region, playerName, playerId, self._playerIdToData)
                    )
                    vehicleInfoTasks.add(task)
                    task.start()

            logInfo("Vehicle info task count: %d." % len(vehicleInfoTasks))

            for task in vehicleInfoTasks:
                task.join()

            logInfo("Tasks are joined.")
        except BaseException:
            logError("Can't load recent stats by vehicle list.", traceback.format_exc())

        withStat = 0
        withRecentStat = 0
        withoutStat = 0

        for _vehicleID, vehicleData in vehicles.iteritems():
            if "accountDBID" in vehicleData:
                playerId = vehicleData["accountDBID"]

                if playerId in self._playerIdToData:
                    withStat += 1

                    if self._playerIdToData[playerId].hasRecentStat:
                        withRecentStat += 1
                else:
                    withoutStat += 1

        logInfo("Stats loaded. With stats: %s, with recent stats: %s, without stats: %s." % (withStat, withRecentStat, withoutStat))

    def formatPlayerName(self, accountDBID, playerName):
        # type: (int, str) -> str
        playerInfo = self._playerIdToData.get(accountDBID, None)
        if playerInfo is not None:
            formattedPlayerStat = self._configFormat.playerName.format(**playerInfo.createDict())
            newPlayerName = formattedPlayerStat + playerName
            # newPlayerName = formattedPlayerName(playerName, configFormat)
            return newPlayerName

        return playerName
