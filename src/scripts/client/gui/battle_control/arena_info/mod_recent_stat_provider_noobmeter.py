# -*- coding: utf-8 -*-
# https://www.apache.org/licenses/LICENSE-2.0.html

import traceback

from mod_recent_stat_constant import PLAYER_ID_NOT_KNOWN
from mod_recent_stat_network import getSiteText, getNextRowCells, getNumberFromCell


def getPlayerId(idSiteText, nickname):
    try:
        nameTitle = "<h1>%s</h1>" % nickname
        nameTitleEndIndex = idSiteText.find(nameTitle) + len(nameTitle)
        idStartIndex = idSiteText.find("<!--", nameTitleEndIndex) + len("<!--")
        idEndIndex = idSiteText.find("-->", idStartIndex) - 1
        return int(idSiteText[idStartIndex:idEndIndex].strip())
    except Exception as e:
        print "[---! The Recent Stat of You] Can't get id from text. Reason: %s" % traceback.format_exc()
        return -1


def getStatistics(region, nickname, playerId):
    if playerId == PLAYER_ID_NOT_KNOWN:
        idSiteText = getSiteText("http://www.noobmeter.com/player/%s/%s" % (region, nickname))
        playerId = getPlayerId(idSiteText, nickname)
        print "[--- The Recent Stat of You] Player ID of %s = %s" % (nickname, playerId)

    siteText = getSiteText("http://www.noobmeter.com/player/%s/%s/%d" % (region, nickname, playerId))
    siteText = siteText.replace("&nbsp;", " ").replace('"', "'")

    try:
        MAX_ITERATIONS = 1000
        iterations = 0

        tableBeginIdx = 0
        while True:
            tableBeginIdx = siteText.find("<table", tableBeginIdx + 1)
            classBeginIdx = siteText.find("'tablesorter'", tableBeginIdx)
            endTableBeginIdx = siteText.find(">", tableBeginIdx)
            if classBeginIdx < endTableBeginIdx:
                break

            assert iterations < MAX_ITERATIONS
            iterations += 1

        headerEndIdx = siteText.find("</tr>", tableBeginIdx)

        ths = getNextRowCells(siteText, tableBeginIdx, "th")

        overallCol = -1
        recentCol = -1

        for i, th in enumerate(ths):
            if "Общий" in th or "Overall" in th:
                overallCol = i
            if "~1000" in th or "~1,000" in th:
                recentCol = i

        tableEndIdx = siteText.find("</table>", headerEndIdx)

        trBeginIdx = headerEndIdx

        wn8 = ""
        battlesRecent = None
        battlesOverall = ""

        while trBeginIdx != -1 and trBeginIdx < tableEndIdx:
            tds = getNextRowCells(siteText, trBeginIdx)
            if len(tds) != 0:
                loweredRowTitle = tds[0].lower()

                if "wn8" in loweredRowTitle:
                    if recentCol != -1:
                        wn8ParsedStr = getNumberFromCell(tds[recentCol])
                    else:
                        wn8ParsedStr = getNumberFromCell(tds[overallCol])

                    if wn8ParsedStr is not None:
                        wn8 = wn8ParsedStr
                elif "battles:" in loweredRowTitle or "кол. боёв:" in loweredRowTitle:
                    if recentCol != -1:
                        battlesRecent = getNumberFromCell(tds[recentCol])

                    battlesOverall = getNumberFromCell(tds[overallCol])
                    pass

            trBeginIdx = siteText.find("<tr", trBeginIdx + 1)

            assert iterations < MAX_ITERATIONS
            iterations += 1

        playerStat = wn8 + "["
        if battlesRecent is not None:
            playerStat += battlesRecent + "/"
        playerStat += str(int(round(int(battlesOverall) / 1000))) + "k]"

        return playerStat
    except Exception:
        print "[--- The Recent Stat of You] Error in getStatistics(%s, %s, %s):" % (region, nickname, playerId)
        print traceback.format_exc()
        return "[?-?]"

