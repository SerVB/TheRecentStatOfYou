# -*- coding: utf-8 -*-
# https://www.apache.org/licenses/LICENSE-2.0.html

import traceback

from mod_recent_stat_config import REGION_SETTING, PROVIDER, NAME_FORMAT_NO_RECENT, NAME_FORMAT_RECENT
from mod_recent_stat_constant import PLAYER_ID_NOT_KNOWN, STAT_FIELDS
from mod_recent_stat_logging import logInfo, logError

_formatted = dict()  # {playerName: formattedPlayerName}


def _formatBattles(strBattles):
    return str(int(round(int(strBattles) / 1000.0))) + "k"


def _formatPlayerData(playerData):
    if playerData.get(STAT_FIELDS.OVERALL_BATTLES, None) is not None:
        playerData[STAT_FIELDS.OVERALL_BATTLES] = _formatBattles(playerData[STAT_FIELDS.OVERALL_BATTLES])

    if playerData.get(STAT_FIELDS.RECENT_WN8, None) is None or playerData.get(STAT_FIELDS.RECENT_BATTLES, None) is None:
        formatted = NAME_FORMAT_NO_RECENT.format(**playerData)
    else:
        formatted = NAME_FORMAT_RECENT.format(**playerData)

    if "{" in formatted:
        return "[?-?]"
    else:
        return formatted


def _updatePlayerName(playerName, playerId):
    playerData = PROVIDER.getStatistics(REGION_SETTING, playerName, playerId)
    newName = _formatPlayerData(playerData) + playerName
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

                if playerName in _formatted and not forced:
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
