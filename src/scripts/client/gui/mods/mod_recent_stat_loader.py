# -*- coding: utf-8 -*-
# https://www.apache.org/licenses/LICENSE-2.0.html

from copy import deepcopy
from threading import Thread
import time
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

        self._welcomeMessage = self._loadWelcomeMessage()
        self._infoMessage = self._loadInfoMessage()

        logInfo("Mod loading is finished: main = %s, format = %s." % (self._configMain, self._configFormat))

    def getWelcomeMessage(self):
        return deepcopy(self._welcomeMessage)

    def getInfoMessage(self):
        return deepcopy(self._infoMessage)

    @staticmethod
    def _loadWelcomeMessage():
        defaultMessage = {
            "message": {
                "message": "The Recent Stat of You<br>Info: <a href='#'>https://github.com/SerVB/TheRecentStatOfYou</a><br>Donate: <a href='#'>https://github.com/SerVB/donate</a>",
                "icon": "../maps/icons/library/MessageIcon-1.png"
            },
            "notify": False
        }

        return defaultMessage

    def _loadInfoMessage(self):
        return {
            "message": {
                "message": "Configs:<br><br>main = %s<br><br>format = %s" % (self._configMain, self._configFormat),
                "icon": "../maps/icons/library/MessageIcon-1.png"
            },
            "notify": False
        }

    def loadPlayerDataByVehicleList(self, vehicles):
        # type: (dict) -> None
        startTime = time.time()
        self._wgStats.loadPlayerDataByVehicleList(vehicles, self._playerIdToData)

        try:
            vehicleInfoTasks = set()

            for _vehicleID, vehicleData in vehicles.iteritems():
                if "name" in vehicleData and "accountDBID" in vehicleData:
                    playerName = vehicleData["name"]
                    playerId = vehicleData["accountDBID"]

                    if playerId in self._playerIdToData and self._playerIdToData[playerId].hasRecentStat:
                        continue

                    for provider in self._configMain.recentStatProviders:
                        task = Thread(
                            target=provider.getStatistics,
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

        logInfo("Stats loaded in %s ms. With stats: %s, with recent stats: %s, without stats: %s." % (int(round((time.time() - startTime) * 1000)), withStat, withRecentStat, withoutStat))

    def formatPlayerName(self, accountDBID, playerName):
        # type: (int, str) -> str
        playerInfo = self._playerIdToData.get(accountDBID, None)
        if playerInfo is not None:
            try:
                formattedPlayerStat = self._configFormat.playerName.format(**playerInfo.createDict(self._configFormat))
                newPlayerName = formattedPlayerStat + playerName
                return newPlayerName
            except BaseException:
                logError("Can't format player name", traceback.format_exc())
                return playerName

        return playerName
