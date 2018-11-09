# -*- coding: utf-8 -*-
# https://www.apache.org/licenses/LICENSE-2.0.html

import json
import traceback

from mod_recent_stat_config_main import ConfigMain
from mod_recent_stat_config_wg_id import ConfigWgId
from mod_recent_stat_container import PlayerData
from mod_recent_stat_converter import formatBattlesToKiloBattles, getXWN8
from mod_recent_stat_logging import logError
from mod_recent_stat_network import getJsonText


class WgStats:
    _ACCOUNT_INFO_URL = "https://api.worldoftanks.{region}/wot/account/info/?application_id={appId}&fields=statistics.all.battles%2Cstatistics.all.wins%2Cstatistics.all.damage_dealt%2Cstatistics.all.frags%2Cstatistics.all.spotted%2Cstatistics.all.capture_points%2Cstatistics.all.dropped_capture_points&account_id={joinedIds}"
    _ACCOUNT_TANK_URL = "https://api.worldoftanks.{region}/wot/account/tanks/?application_id={appId}&fields=statistics.battles%2Ctank_id&account_id={joinedIds}"

    def __init__(self, configMain, configWgId):
        # type: (ConfigMain, ConfigWgId) -> None
        self._wn8Expected = None
        self._configMain = configMain
        self._configWgId = configWgId

        self.loadWn8Expected()

    def loadWn8Expected(self):
        # type: () -> None
        if self._wn8Expected is None:
            url = "http://www.wnefficiency.net/exp/expected_tank_values_latest.json"
            wn8ExpectedData = json.loads(getJsonText(url))["data"]
            self._wn8Expected = dict()

            for item in wn8ExpectedData:
                idNum = item["IDNum"]
                self._wn8Expected[idNum] = item
                self._wn8Expected[idNum].pop("IDNum")

    def loadPlayerDataByVehicleList(self, vehicles, playerIdToData):
        # type: (dict, dict) -> None
        idsToBeLoaded = set()

        for _vehicleID, vehicleData in vehicles.iteritems():
            if "accountDBID" in vehicleData:
                playerId = vehicleData["accountDBID"]

                if playerId in playerIdToData:
                    continue

                idsToBeLoaded.add(playerId)

        for playerId in idsToBeLoaded:
            playerIdToData[playerId] = PlayerData()

        joinedIds = ",".join(map(str, idsToBeLoaded))

        accountsInfoUrl = self._ACCOUNT_INFO_URL \
            .format(region=self._configMain.region, appId=self._configWgId.wgId, joinedIds=joinedIds)

        accountsTanksUrl = self._ACCOUNT_TANK_URL \
            .format(region=self._configMain.region, appId=self._configWgId.wgId, joinedIds=joinedIds)

        try:
            accountsInfo = json.loads(getJsonText(accountsInfoUrl, self._configMain.timeout)).get("data", None)
            accountsTanks = json.loads(getJsonText(accountsTanksUrl, self._configMain.timeout)).get("data", None)
        except BaseException:
            logError("Error loading statistics...", traceback.format_exc())
        else:
            for playerId in idsToBeLoaded:
                strPlayerId = str(playerId)
                if strPlayerId in accountsInfo and accountsInfo[strPlayerId]["statistics"]["all"]["battles"] != 0:
                    currentAccountInfo = accountsInfo[strPlayerId]
                    battles = currentAccountInfo["statistics"]["all"]["battles"]

                    playerData = playerIdToData[playerId]
                    playerData.battles = battles
                    playerData.kb = formatBattlesToKiloBattles(battles)
                    playerData.wn8 = 0
                    playerData.xwn8 = 0

                    if strPlayerId in accountsTanks and battles != 0:
                        floatBattles = float(battles)

                        winrate = currentAccountInfo["statistics"]["all"]["wins"] * 100.0 / floatBattles
                        avgDmg = currentAccountInfo["statistics"]["all"]["damage_dealt"] / floatBattles
                        avgFrags = currentAccountInfo["statistics"]["all"]["frags"] / floatBattles
                        avgSpot = currentAccountInfo["statistics"]["all"]["spotted"] / floatBattles
                        avgDef = currentAccountInfo["statistics"]["all"]["dropped_capture_points"] / floatBattles

                        wn8 = self.getWN8(winrate, avgDmg, avgFrags, avgSpot, avgDef, accountsTanks[strPlayerId], self._wn8Expected)

                        playerData.wn8 = wn8
                        playerData.xwn8 = getXWN8(wn8)

    @staticmethod
    def getWN8(winrate, avgDmg, avgFrags, avgSpot, avgDef, accountTanks, wn8Expected):
        # type: (float, float, float, float, float, dict, dict) -> int
        if wn8Expected is None:
            return 0

        eFrags = 0
        eDmg = 0
        eSpot = 0
        eDef = 0
        eWinrate = 0
        eBattles = 0

        for accountTank in accountTanks:
            tankBattles = accountTank["statistics"]["battles"]
            tankId = accountTank["tank_id"]

            if tankId in wn8Expected:
                tankData = wn8Expected[tankId]

                eFrags += tankBattles * tankData["expFrag"]
                eDmg += tankBattles * tankData["expDamage"]
                eSpot += tankBattles * tankData["expSpot"]
                eDef += tankBattles * tankData["expDef"]
                eWinrate += tankBattles * tankData["expWinRate"]
                eBattles += tankBattles

        if 0 in (eWinrate, eDmg, eFrags, eSpot, eDef):
            return 0

        rWin = max(((winrate * eBattles / eWinrate - 0.71) / (1 - 0.71)), 0)
        rDmg = max(((avgDmg * eBattles / eDmg - 0.22) / (1 - 0.22)), 0)
        rFrag = max(min(rDmg + 0.2, ((avgFrags * eBattles / eFrags - 0.12) / (1 - 0.12))), 0)
        rSpot = max(min(rDmg + 0.1, ((avgSpot * eBattles / eSpot - 0.38) / (1 - 0.38))), 0)
        rDef = max(min(rDmg + 0.1, ((avgDef * eBattles / eDef - 0.10) / (1 - 0.10))), 0)

        return int(round(980 * rDmg + 210 * rDmg * rFrag + 155 * rFrag * rSpot + 75 * rDef * rFrag + 145 * min(1.8, rWin)))
