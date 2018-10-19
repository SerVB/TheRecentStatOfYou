# -*- coding: utf-8 -*-
# https://www.apache.org/licenses/LICENSE-2.0.html

from gui.battle_control.arena_info.arena_dp import ArenaDataProvider
from gui.battle_control.arena_info.player_format import PlayerFullNameFormatter, PlayerFormatResult

from mod_recent_stat_logging import logInfo
from mod_recent_stat_container import updatePlayerFormatByVehicleList, formattedPlayerName


logInfo("Mod loading started")


def buildVehiclesDataNew(self, vehicles):
    updatePlayerFormatByVehicleList(vehicles)
    buildVehiclesDataOld(self, vehicles)


buildVehiclesDataOld = ArenaDataProvider.buildVehiclesData
ArenaDataProvider.buildVehiclesData = buildVehiclesDataNew


def player_formatNew(self, vInfoVO, playerName=None):
    result = player_formatOld(self, vInfoVO, playerName)
    playerName = formattedPlayerName(result.playerName)
    return PlayerFormatResult(result.playerFullName, playerName, result.clanAbbrev, result.regionCode, result.vehicleName)


player_formatOld = PlayerFullNameFormatter.format
PlayerFullNameFormatter.format = player_formatNew


logInfo("Mod loading finished")
