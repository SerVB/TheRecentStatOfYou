# -*- coding: utf-8 -*-
# https://www.apache.org/licenses/LICENSE-2.0.html

from gui.battle_control.arena_info.arena_dp import ArenaDataProvider
from gui.battle_control.arena_info.player_format import PlayerFullNameFormatter, PlayerFormatResult
from notification.NotificationListView import NotificationListView

from mod_recent_stat_loader import ModRecentStat
from mod_recent_stat_logging import logInfo


logInfo("Mod initialization is started.")

modRecentStat = ModRecentStat()


def buildVehiclesDataNew(self, vehicles):
    modRecentStat.loadPlayerDataByVehicleList(vehicles)
    buildVehiclesDataOld(self, vehicles)


buildVehiclesDataOld = ArenaDataProvider.buildVehiclesData
ArenaDataProvider.buildVehiclesData = buildVehiclesDataNew


def formatNew(self, vInfoVO, playerName=None):
    result = formatOld(self, vInfoVO, playerName)
    accountDBID = vInfoVO.player.accountDBID

    newPlayerName = modRecentStat.formatPlayerName(accountDBID, result.playerName)

    return PlayerFormatResult(result.playerFullName, newPlayerName, result.clanAbbrev, result.regionCode, result.vehicleName)


formatOld = PlayerFullNameFormatter.format
PlayerFullNameFormatter.format = formatNew


def nlv_getMessagesListNew(self):
    result = nlv_getMessagesListOld(self)

    result.insert(0, modRecentStat.getWelcomeMessage())

    return result


nlv_getMessagesListOld = NotificationListView._NotificationListView__getMessagesList
NotificationListView._NotificationListView__getMessagesList = nlv_getMessagesListNew

logInfo("Mod initialization is finished.")
