# -*- coding: utf-8 -*-
# https://www.apache.org/licenses/LICENSE-2.0.html

import json
import traceback

from mod_recent_stat_constant import PLAYER_ID_NOT_KNOWN, STAT_FIELDS
from mod_recent_stat_logging import logInfo, logError
from mod_recent_stat_network import getRawSiteText, getFormattedHtmlText, getJsonText
from mod_recent_stat_provider import StatProvider


class Kttc(StatProvider):
    @staticmethod
    def _getPlayerId(mainSiteText):
        methodCallBeginIdx = mainSiteText.find("kttc.account.init(")
        assert methodCallBeginIdx != -1, "No method call found"

        methodCallEndIdx = mainSiteText.find("</script>", methodCallBeginIdx)
        assert methodCallEndIdx != -1, "No method end found"

        accountIdx = mainSiteText.find("'accountId'", methodCallBeginIdx, methodCallEndIdx)
        assert accountIdx != -1, "No accountId found"

        startIdx = accountIdx
        for _ in range(3):
            startIdx = mainSiteText.find("'", startIdx, methodCallEndIdx) + 1

        endIdx = mainSiteText.find("'", startIdx, methodCallEndIdx)
        answer = int(mainSiteText[startIdx:endIdx])
        return int(answer)

    def _getStatistics(self, region, nickname, playerId):
        if playerId == PLAYER_ID_NOT_KNOWN:
            mainSiteText = getFormattedHtmlText("https://kttc.ru/wot/%s/user/%s/" % (region, nickname))
            playerId = self._getPlayerId(mainSiteText)
            logInfo("Player ID of %s = %s" % (nickname, playerId))

        overallJson = json.loads(getJsonText("https://kttc.ru/wot/%s/user/%s/get-user-json/%s/" % (region, nickname, playerId)))
        assert overallJson["success"], "Overall json isn't successful: %s" % overallJson

        playerData = {
            STAT_FIELDS.RECENT_BATTLES: None,
            STAT_FIELDS.RECENT_WN8: None,
            STAT_FIELDS.OVERALL_BATTLES: overallJson["data"]["currentBattles"],
            STAT_FIELDS.OVERALL_WN8: overallJson["data"]["wn8"]
        }

        recentStatJson = json.loads(getJsonText("https://kttc.ru/wot/ru/user/%s/get-by-battles/%s/" % (nickname, playerId)))
        if recentStatJson["success"] and "1000" in recentStatJson["data"]:
            if recentStatJson["data"]["1000"]["BT"] != 0:  # Filter not valid recent stats
                playerData[STAT_FIELDS.RECENT_BATTLES] = str(recentStatJson["data"]["1000"]["BT"])
                playerData[STAT_FIELDS.RECENT_WN8] = str(int(round(recentStatJson["data"]["1000"]["WN8"])))

        return playerData
