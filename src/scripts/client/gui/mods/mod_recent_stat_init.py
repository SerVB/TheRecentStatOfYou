# -*- coding: utf-8 -*-
# https://www.apache.org/licenses/LICENSE-2.0.html

import traceback

from gui.battle_control.arena_info.arena_dp import ArenaDataProvider
from gui.battle_control.arena_info.player_format import PlayerFullNameFormatter, PlayerFormatResult
from notification.NotificationListView import NotificationListView

from mod_recent_stat_loader import ModRecentStat
from mod_recent_stat_logging import logInfo, logError


logInfo("Mod initialization is started.")

modRecentStat = ModRecentStat()


def buildVehiclesDataNew(self, vehicles):
    try:
        modRecentStat.loadPlayerDataByVehicleList(vehicles)
    except BaseException:
        logError("Error in buildVehiclesDataNew", traceback.format_exc())

    buildVehiclesDataOld(self, vehicles)


ArenaDataProvider.buildVehiclesData, buildVehiclesDataOld = buildVehiclesDataNew, ArenaDataProvider.buildVehiclesData


def formatNew(self, vInfoVO, playerName=None):
    result = formatOld(self, vInfoVO, playerName)
    newPlayerName = result.playerName

    try:
        accountDBID = vInfoVO.player.accountDBID
        newPlayerName = modRecentStat.formatPlayerName(accountDBID, result.playerName)
    except BaseException:
        logError("Error in formatNew", traceback.format_exc())

    return PlayerFormatResult(result.playerFullName, newPlayerName, result.clanAbbrev, result.regionCode, result.vehicleName)


PlayerFullNameFormatter.format, formatOld = formatNew, PlayerFullNameFormatter.format


def nlv_getMessagesListNew(self):
    result = nlv_getMessagesListOld(self)

    try:
        result.insert(0, modRecentStat.getWelcomeMessage())
        result.insert(1, modRecentStat.getInfoMessage())
    except BaseException:
        logError("Error in nlv_getMessagesListNew", traceback.format_exc())

    return result


NotificationListView._NotificationListView__getMessagesList, nlv_getMessagesListOld = nlv_getMessagesListNew, NotificationListView._NotificationListView__getMessagesList

logInfo("Mod initialization is finished.")
