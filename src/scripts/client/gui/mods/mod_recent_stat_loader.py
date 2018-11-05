# -*- coding: utf-8 -*-
# https://www.apache.org/licenses/LICENSE-2.0.html

from gui.battle_control.arena_info.arena_dp import ArenaDataProvider
from gui.battle_control.arena_info.player_format import PlayerFullNameFormatter, PlayerFormatResult

from mod_recent_stat_config_format import ConfigFormat
from mod_recent_stat_config_main import ConfigMain
from mod_recent_stat_config_wg_id import ConfigWgId
# from mod_recent_stat_container import updatePlayerFormatByVehicleList, formattedPlayerName
from mod_recent_stat_logging import logInfo
from mod_recent_stat_wg_stats import WgStats


logInfo("Mod loading started")

configFormat = ConfigFormat()
configMain = ConfigMain()
configWgId = ConfigWgId()
playerIdToData = dict()
wgStats = WgStats(configMain, configWgId, playerIdToData)


def buildVehiclesDataNew(self, vehicles):
    wgStats.loadPlayerDataByVehicleList(vehicles)
    # updatePlayerFormatByVehicleList(vehicles)
    buildVehiclesDataOld(self, vehicles)


buildVehiclesDataOld = ArenaDataProvider.buildVehiclesData
ArenaDataProvider.buildVehiclesData = buildVehiclesDataNew


def formatNew(self, vInfoVO, playerName=None):
    result = formatOld(self, vInfoVO, playerName)
    accountDBID = vInfoVO.player.accountDBID
    playerInfo = wgStats.playerIdToData.get(accountDBID, None)
    if playerInfo is not None:
        playerName = str(playerInfo["xwn8"]) + " " + str(playerInfo["kb"]) + "k " + result.playerName

    # playerName = formattedPlayerName(result.playerName, configFormat)
    return PlayerFormatResult(result.playerFullName, playerName, result.clanAbbrev, result.regionCode, result.vehicleName)


formatOld = PlayerFullNameFormatter.format
PlayerFullNameFormatter.format = formatNew


logInfo("Mod loading finished")
