# -*- coding: utf-8 -*-
# https://www.apache.org/licenses/LICENSE-2.0.html

import traceback
import json

from mod_recent_stat_constant import PLAYER_ID_NOT_KNOWN
from mod_recent_stat_logging import logInfo, logError
from mod_recent_stat_network import getRawSiteText, getFormattedHtmlText, getJsonText


def _getStatTable(mainSiteText):
    methodCallBeginIdx = mainSiteText.find("kttc.account.init(")
    assert methodCallBeginIdx != -1, "No method call found"

    methodCallEndIdx = mainSiteText.find("</script>", methodCallBeginIdx)
    assert methodCallEndIdx != -1, "No method end found"

    statTableBeginIdx = mainSiteText.find("statTable", methodCallBeginIdx, methodCallEndIdx)
    assert statTableBeginIdx != -1, "No statTable found"

    jsonBeginIdx = mainSiteText.find("[{", statTableBeginIdx, methodCallEndIdx) + 1
    assert jsonBeginIdx != -1, "No statTable begin found"

    jsonEndIdx = mainSiteText.find("}", jsonBeginIdx, methodCallEndIdx) + 1  # To the end of first section
    assert jsonEndIdx != -1, "No statTable end found"

    jsonText = mainSiteText[jsonBeginIdx:jsonEndIdx]
    return json.loads(jsonText.replace("'", '"'))


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


def getStatistics(region, nickname, playerId):
    try:
        if playerId == PLAYER_ID_NOT_KNOWN:
            mainSiteText = getFormattedHtmlText("https://kttc.ru/wot/%s/user/%s/" % (region, nickname))
            playerId = _getPlayerId(mainSiteText)
            logInfo("Player ID of %s = %s" % (nickname, playerId))

        _updateStatus = getRawSiteText("https://kttc.ru/wot/%s/statistics/user/update/%s/" % (region, playerId))

        overallJson = json.loads(getJsonText("https://kttc.ru/wot/%s/user/%s/get-user-json/%s/" % (region, nickname, playerId)))
        assert overallJson["success"], "Overall json isn't successful: %s" % overallJson

        wn8 = overallJson["data"]["wn8"]
        battlesOverall = overallJson["data"]["currentBattles"]
        battlesRecent = None

        recentStatJson = json.loads(getJsonText("https://kttc.ru/wot/ru/user/%s/get-by-battles/%s/" % (nickname, playerId)))
        if recentStatJson["success"] and "1000" in recentStatJson["data"]:
            battlesRecent = recentStatJson["data"]["1000"]["BT"]
            if battlesRecent == 0:  # Filter not valid recent stats
                battlesRecent = None
            else:
                battlesRecent = str(battlesRecent)
                wn8 = str(int(round(recentStatJson["data"]["1000"]["WN8"])))

        playerStat = wn8 + "["
        if battlesRecent is not None:
            playerStat += battlesRecent + "/"
        playerStat += str(int(round(int(battlesOverall) / 1000.0))) + "k]"

        return playerStat
    except BaseException:
        logError("Error in getStatistics(%s, %s, %s)" % (region, nickname, playerId), traceback.format_exc())
        return "[?-?]"
