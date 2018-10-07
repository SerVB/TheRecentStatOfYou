# -*- coding: utf-8 -*-
# https://www.apache.org/licenses/LICENSE-2.0.html

import traceback

from mod_recent_stat_config import REGION_SETTING, GET_STATISTICS
from mod_recent_stat_constant import PLAYER_ID_NOT_KNOWN
from mod_recent_stat_logging import logInfo, logError

_formatted = dict()  # {playerName: formattedPlayerName}


def _updatePlayerName(playerName, playerId):
    playerStat = GET_STATISTICS(REGION_SETTING, playerName, playerId)
    newName = playerStat + playerName
    _formatted[playerName] = newName


def formattedPlayerName(playerName):
    return _formatted.get(playerName, "[?]" + playerName)


def updatePlayerFormatByVehicleList(vehicles, forced=False):
    try:
        from threading import Thread

        vehicleInfoTasks = set()

        for vID, vData in vehicles.iteritems():
            if "name" in vData:
                playerName = vData["name"]

                if not forced and playerName in _formatted:
                    continue

                playerId = vData.get("accountDBID", PLAYER_ID_NOT_KNOWN)

                task = Thread(target=_updatePlayerName, args=(playerName, playerId))
                vehicleInfoTasks.add(task)
                task.start()

        logInfo("Vehicle info task count: %d" % len(vehicleInfoTasks))

        for task in vehicleInfoTasks:
            task.join()

        logInfo("Tasks are joined")
    except BaseException:
        logError("Can't update player format by vehicle list", traceback.format_exc())
