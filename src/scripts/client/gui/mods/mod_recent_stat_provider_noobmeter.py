# -*- coding: utf-8 -*-
# https://www.apache.org/licenses/LICENSE-2.0.html

from mod_recent_stat_constant import PLAYER_ID_NOT_KNOWN, COLUMN_ID_NOT_FOUND, MAX_ITERATIONS, STAT_FIELDS
from mod_recent_stat_logging import logInfo
from mod_recent_stat_network import getFormattedHtmlText, getNextRowCells, getNumberFromCell
from mod_recent_stat_provider import StatProvider


class Noobmeter(StatProvider):
    @staticmethod
    def _getPlayerId(idSiteText, nickname):
        # type: (str, str) -> int
        nameTitle = "<h1>%s</h1>" % nickname
        nameTitleEndIndex = idSiteText.find(nameTitle) + len(nameTitle)
        idStartIndex = idSiteText.find("<!--", nameTitleEndIndex) + len("<!--")
        idEndIndex = idSiteText.find("-->", idStartIndex) - 1
        return int(idSiteText[idStartIndex:idEndIndex].strip())

    @staticmethod
    def _getStatTableBeginIdx(siteText):
        # type: (str) -> int
        iterations = 0

        tableBeginIdx = 0
        while True:
            tableBeginIdx = siteText.find("<table", tableBeginIdx + 1)
            classBeginIdx = siteText.find("tablesorter", tableBeginIdx)
            endTableBeginIdx = siteText.find(">", tableBeginIdx)
            if classBeginIdx < endTableBeginIdx:
                break

            assert iterations < MAX_ITERATIONS, "Too many iterations: %s" % iterations
            iterations += 1

        return tableBeginIdx

    @staticmethod
    def _getOverallAndRecentColumnIdx(siteText, tableBeginIdx):
        # type: (str, int) -> (int, int)
        ths = getNextRowCells(siteText, tableBeginIdx, "th")

        overallColumnIdx = COLUMN_ID_NOT_FOUND
        recentColumnIdx = COLUMN_ID_NOT_FOUND

        for i, th in reversed(tuple(enumerate(ths))):
            if "Общий" in th or "Overall" in th:
                overallColumnIdx = i
            if "~1000" in th or "~1,000" in th:
                recentColumnIdx = i

        assert overallColumnIdx != COLUMN_ID_NOT_FOUND, "No overall column found in %s" % ths

        return overallColumnIdx, recentColumnIdx

    @staticmethod
    def _getTrsWithData(siteText, tableBeginIdx):
        # type: (str, int) -> list
        iterations = 0

        headerEndIdx = siteText.find("</tr>", tableBeginIdx)
        tableEndIdx = siteText.find("</table>", headerEndIdx)
        nextTrBeginIdx = headerEndIdx

        trs = list()

        while nextTrBeginIdx != -1 and nextTrBeginIdx < tableEndIdx:
            nowTrBeginIdx = nextTrBeginIdx

            tds = getNextRowCells(siteText, nowTrBeginIdx)
            trs.append(tds)

            nextTrBeginIdx = siteText.find("<tr", nowTrBeginIdx + 1)

            assert iterations < MAX_ITERATIONS, "Too many iterations: %s" % iterations
            iterations += 1

        return trs

    def _getStatistics(self, region, nickname, playerId):
        # type: (str, str, str) -> dict
        if playerId == PLAYER_ID_NOT_KNOWN:
            idSiteText = getFormattedHtmlText("https://www.noobmeter.com/player/%s/%s" % (region, nickname))
            playerId = self._getPlayerId(idSiteText, nickname)
            logInfo("Player ID of %s = %s" % (nickname, playerId))

        siteText = getFormattedHtmlText("https://www.noobmeter.com/player/%s/%s/%d" % (region, nickname, playerId))

        tableBeginIdx = self._getStatTableBeginIdx(siteText)
        overallColumnIdx, recentColumnIdx = self._getOverallAndRecentColumnIdx(siteText, tableBeginIdx)
        trs = self._getTrsWithData(siteText, tableBeginIdx)

        playerData = {
            STAT_FIELDS.RECENT_BATTLES: None,
            STAT_FIELDS.RECENT_WN8: None,
            STAT_FIELDS.OVERALL_BATTLES: None,
            STAT_FIELDS.OVERALL_WN8: None
        }

        for tds in trs:
            if len(tds) != 0:
                loweredRowTitle = tds[0].lower()

                if "wn8" in loweredRowTitle:
                    if recentColumnIdx != COLUMN_ID_NOT_FOUND:
                        playerData[STAT_FIELDS.RECENT_WN8] = getNumberFromCell(tds[recentColumnIdx])

                    playerData[STAT_FIELDS.OVERALL_WN8] = getNumberFromCell(tds[overallColumnIdx])
                elif "battles:" in loweredRowTitle or "кол. боёв:" in loweredRowTitle:
                    if recentColumnIdx != COLUMN_ID_NOT_FOUND:
                        playerData[STAT_FIELDS.RECENT_BATTLES] = getNumberFromCell(tds[recentColumnIdx])

                    playerData[STAT_FIELDS.OVERALL_BATTLES] = getNumberFromCell(tds[overallColumnIdx])

        return playerData

