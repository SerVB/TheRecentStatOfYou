# -*- coding: utf-8 -*-
# https://www.apache.org/licenses/LICENSE-2.0.html

from gui.battle_control.arena_info.arena_dp import ArenaDataProvider
from gui.battle_control.arena_info.player_format import PlayerFullNameFormatter, PlayerFormatResult

from mod_recent_stat_logging import logInfo
from mod_recent_stat_container import updatePlayerFormatByVehicleList, formattedPlayerName


logInfo("Mod loading started")


def new_buildVehiclesData(self, vehicles):
    updatePlayerFormatByVehicleList(vehicles)
    old_buildVehiclesData(self, vehicles)


old_buildVehiclesData = ArenaDataProvider.buildVehiclesData
ArenaDataProvider.buildVehiclesData = new_buildVehiclesData


def new_player_format(self, vInfoVO, playerName=None):
    result = old_player_format(self, vInfoVO, playerName)
    playerName = formattedPlayerName(result.playerName)
    return PlayerFormatResult(result.playerFullName, playerName, result.clanAbbrev, result.regionCode, result.vehicleName)


old_player_format = PlayerFullNameFormatter.format
PlayerFullNameFormatter.format = new_player_format


logInfo("Mod loading finished")
