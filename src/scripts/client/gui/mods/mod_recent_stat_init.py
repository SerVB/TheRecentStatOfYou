# -*- coding: utf-8 -*-
# https://www.apache.org/licenses/LICENSE-2.0.html

from gui.battle_control.arena_info.arena_dp import ArenaDataProvider
from gui.battle_control.arena_info.player_format import PlayerFullNameFormatter, PlayerFormatResult

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

logInfo("Mod initialization is finished.")
