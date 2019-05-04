# -*- coding: utf-8 -*-
# https://www.apache.org/licenses/LICENSE-2.0.html

import traceback
import re

import BigWorld
from gui.battle_control.arena_info.arena_dp import ArenaDataProvider
from gui.battle_control.arena_info.player_format import PlayerFullNameFormatter, PlayerFormatResult
from gui.SystemMessages import SM_TYPE, pushMessage
from gui.Scaleform.daapi.view.lobby.LobbyView import LobbyView
from notification.settings import NOTIFICATION_TYPE
from notification.actions_handlers import NotificationsActionsHandlers

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

    return PlayerFormatResult(result.playerFullName, newPlayerName, result.clanAbbrev, result.regionCode,
                              result.vehicleName)


PlayerFullNameFormatter.format, formatOld = formatNew, PlayerFullNameFormatter.format


def handleActionNew(self, model, typeID, entityID, actionName):
    needOpen = False

    try:
        needOpen = typeID == NOTIFICATION_TYPE.MESSAGE and re.match('https?://', actionName, re.I)
        if needOpen:
            BigWorld.wg_openWebBrowser(actionName)
    except BaseException:
        logError("Error in handleActionNew", traceback.format_exc())

    if not needOpen:
        handleActionOld(self, model, typeID, entityID, actionName)


NotificationsActionsHandlers.handleAction, handleActionOld = handleActionNew, NotificationsActionsHandlers.handleAction


def LobbyView_populateNew(self):
    LobbyView_populateOld(self)

    try:
        if not modRecentStat.notificationsShowed:
            modRecentStat.notificationsShowed = True

            pushMessage(modRecentStat.getWelcomeMessage(), SM_TYPE.Information)
            pushMessage(modRecentStat.getInfoMessage(), SM_TYPE.Information)
    except BaseException:
        logError("Error in LobbyView_populateNew", traceback.format_exc())


LobbyView._populate, LobbyView_populateOld = LobbyView_populateNew, LobbyView._populate

logInfo("Mod initialization is finished.")
