# -*- coding: utf-8 -*-
# https://www.apache.org/licenses/LICENSE-2.0.html

import string
import traceback

from mod_recent_stat_config import PROVIDER
from mod_recent_stat_config_format import ConfigFormat
from mod_recent_stat_config_main import ConfigMain
from mod_recent_stat_constant import PLAYER_ID_NOT_KNOWN, STAT_FIELDS
from mod_recent_stat_converter import formatBattlesToKiloBattles
from mod_recent_stat_logging import logInfo, logError


class PlayerData(object):
    battles = None  # type: [int, None]
    kb = None  # type: [int, None]
    wn8 = None  # type: [int, None]
    xwn8 = None  # type: [int, None]

    hasRecentStat = False  # type: bool

    def createDict(self):
        # type: () -> dict
        return {
            STAT_FIELDS.KILO_BATTLES: self.kb,
            STAT_FIELDS.BATTLES: self.battles,
            STAT_FIELDS.WN8: self.wn8,
            STAT_FIELDS.XWN8: self.xwn8,
        }


class SafeDict(dict):
    def __missing__(self, key):
        return "{" + key + "}"


_formatted = dict()  # {playerName: formattedPlayerName}


def _formatPlayerData(playerData, configFormat):
    # type: (dict, ConfigFormat) -> str
    if playerData.get(STAT_FIELDS.KILO_BATTLES, None) is not None:
        playerData[STAT_FIELDS.KILO_BATTLES] = formatBattlesToKiloBattles(playerData[STAT_FIELDS.KILO_BATTLES])

    if playerData.get(STAT_FIELDS.WN8, None) is None or playerData.get(STAT_FIELDS.KILO_BATTLES, None) is None:
        formatted = string.Formatter().vformat(configFormat.playerName, (), SafeDict(**playerData))
    else:
        formatted = string.Formatter().vformat(configFormat.playerName, (), SafeDict(**playerData))
    if "{" in formatted:
        return configFormat.noInfo
    else:
        return formatted


def _updatePlayerName(playerName, playerId, configFormat, configMain):
    # type: (str, str, ConfigFormat, ConfigMain) -> None
    playerData = PROVIDER.getStatistics(configMain.region, playerName, playerId)
    newName = _formatPlayerData(playerData, configFormat) + playerName
    _formatted[playerName] = newName


def formattedPlayerName(playerName, configFormat):
    # type: (str, ConfigFormat) -> str
    return _formatted.get(playerName, configFormat.noInfo + playerName)


def updatePlayerFormatByVehicleList(vehicles, forced=False):
    # type: (dict, bool) -> None
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
