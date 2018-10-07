# -*- coding: utf-8 -*-
from gui.battle_control.arena_info.arena_dp import ArenaDataProvider
from gui.battle_control.arena_info.player_format import PlayerFullNameFormatter, PlayerFormatResult
import traceback
import json

PLAYER_ID_NOT_KNOWN = -1
COLUMN_ID_NOT_FOUND = -1
MAX_ITERATIONS = 1000
REGION_SETTING = "ru"
GET_STATISTICS = None
_formatted = dict()  # {playerName: formattedPlayerName}

class STAT_PROVIDER:
    NOOBMETER = "noobmeter"
    KTTC = "kttc"

    SUPPORTED = (NOOBMETER, KTTC)
    
    
PROVIDER = STAT_PROVIDER.KTTC

def logInfo(message):
    print "[--- The Recent Stat of You vvv]"
    print message
    print "[--- The Recent Stat of You ^^^]"


def logError(message, exceptionText):
    print "[!--- The Recent Stat of You vvv]"
    print message
    print "[!--- Exception text:]"
    print exceptionText
    print "[!--- The Recent Stat of You ^^^]"
    
    
def getSiteText(url):
    import urllib2
    html = urllib2.urlopen(url=url).read().replace("&nbsp;", " ").replace('"', "'")
    return html


def getNextRowCells(string, idx, td="td"):
    cellBegin = "<%s" % td
    cellEnd = "</%s>" % td

    answer = list()
    rowEndIdx = string.find("</tr>", idx)
    nowTdIdx = string.find(cellBegin, idx, rowEndIdx)
    while nowTdIdx != -1:
        nowTdBeginIdx = string.find(">", nowTdIdx) + 1
        nowTdEndIdx = string.find(cellEnd, nowTdIdx)

        colspan = 1
        colspanBeginIdx = string.find("colspan", nowTdIdx, nowTdBeginIdx)
        if colspanBeginIdx != -1:
            colspanValueBeginIdx = string.find("'", colspanBeginIdx, nowTdBeginIdx) + 1
            assert colspanValueBeginIdx != -1, "No colspan begin found in %s" % string[nowTdIdx:nowTdBeginIdx]
            colspanValueEndIdx = string.find("'", colspanValueBeginIdx, nowTdBeginIdx)
            assert colspanValueEndIdx != -1, "No colspan end found in %s" % string[nowTdIdx:nowTdBeginIdx]
            colspan = int(string[colspanValueBeginIdx:colspanValueEndIdx])

        for _ in range(colspan):
            answer.append(string[nowTdBeginIdx:nowTdEndIdx])

        nowTdIdx = string.find(cellBegin, nowTdEndIdx)

    return answer


def removeTags(text):
    add = True
    answer = ""

    for c in text:
        if c == "<":
            add = False
        elif c == ">":
            add = True
        elif add:
            answer += c

    return answer


# Returns str of number in <td>...</td> or None if not found
def getNumberFromCell(tdText):
    split = removeTags(tdText).replace(",", " ").split()

    data = None

    for i in range(len(split) - 1):
        if split[i].isdigit() and split[i + 1].isdigit():
            data = split[i] + split[i + 1]

            return data

    for i in range(len(split)):
        if split[i].isdigit():
            data = split[i]

    return data
    
                
class Kttc(object):

    def _getStatTable(self, mainSiteText):
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
    
    
    def _getPlayerId(self, mainSiteText):
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
    
    
    def getStatistics(self, region, nickname, playerId):
        try:
            mainSiteText = getSiteText("https://kttc.ru/wot/%s/user/%s/" % (region, nickname))
    
            if playerId == PLAYER_ID_NOT_KNOWN:
                playerId = self._getPlayerId(mainSiteText)
                logInfo("Player ID of %s = %s" % (nickname, playerId))
    
            _updateStatus = getSiteText("https://kttc.ru/wot/%s/statistics/user/update/%s/" % (region, playerId))
    
            mainSiteText = getSiteText("https://kttc.ru/wot/%s/user/%s/" % (region, nickname))
            overallStatTable = self._getStatTable(mainSiteText)
    
            wn8 = str(int(round(overallStatTable["WN8"])))
            battlesOverall = overallStatTable["BT"]
            battlesRecent = None
    
            recentStatJson = json.loads(getSiteText("https://kttc.ru/wot/ru/user/%s/get-by-battles/%s/" % (nickname, playerId)).replace("'", '"'))
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


kttc = Kttc()

class Noobmeter(object):


    def getPlayerId(self, idSiteText, nickname):
        try:
            nameTitle = "<h1>%s</h1>" % nickname
            nameTitleEndIndex = idSiteText.find(nameTitle) + len(nameTitle)
            idStartIndex = idSiteText.find("<!--", nameTitleEndIndex) + len("<!--")
            idEndIndex = idSiteText.find("-->", idStartIndex) - 1
            return int(idSiteText[idStartIndex:idEndIndex].strip())
        except BaseException:
            logError("Can't get id from text", traceback.format_exc())
            return PLAYER_ID_NOT_KNOWN
    
    
    def _getStatTableBeginIdx(self, siteText):
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
    
    
    def _getOverallAndRecentColumnIdx(self, siteText, tableBeginIdx):
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
    
    
    def _getTrsWithData(self, siteText, tableBeginIdx):
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
    
    
    def getStatistics(self, region, nickname, playerId):
        if playerId == PLAYER_ID_NOT_KNOWN:
            idSiteText = getSiteText("http://www.noobmeter.com/player/%s/%s" % (region, nickname))
            playerId = self.getPlayerId(idSiteText, nickname)
            logInfo("Player ID of %s = %s" % (nickname, playerId))
    
        siteText = getSiteText("http://www.noobmeter.com/player/%s/%s/%d" % (region, nickname, playerId))
    
        try:
            tableBeginIdx = self._getStatTableBeginIdx(siteText)
            overallColumnIdx, recentColumnIdx = self._getOverallAndRecentColumnIdx(siteText, tableBeginIdx)
            trs = self._getTrsWithData(siteText, tableBeginIdx)
    
            wn8 = ""
            battlesRecent = None
            battlesOverall = ""
    
            for tds in trs:
                if len(tds) != 0:
                    loweredRowTitle = tds[0].lower()
    
                    if "wn8" in loweredRowTitle:
                        if recentColumnIdx != -1:
                            wn8ParsedStr = getNumberFromCell(tds[recentColumnIdx])
                        else:
                            wn8ParsedStr = getNumberFromCell(tds[overallColumnIdx])
    
                        if wn8ParsedStr is not None:
                            wn8 = wn8ParsedStr
                    elif "battles:" in loweredRowTitle or u"кол. боёв:" in loweredRowTitle:
                        if recentColumnIdx != -1:
                            battlesRecent = getNumberFromCell(tds[recentColumnIdx])
    
                        battlesOverall = getNumberFromCell(tds[overallColumnIdx])
    
            playerStat = wn8 + "["
            if battlesRecent is not None:
                playerStat += battlesRecent + "/"
            playerStat += str(int(round(int(battlesOverall) / 1000.0))) + "k]"
    
            return playerStat
        except BaseException:
            logError("Error in getStatistics(%s, %s, %s)" % (region, nickname, playerId), traceback.format_exc())
            return "[?-?]"


noobmeter = Noobmeter()

if PROVIDER not in STAT_PROVIDER.SUPPORTED:
    assert False, "Stat provider isn't supported: %s" % PROVIDER
elif PROVIDER == STAT_PROVIDER.KTTC:
    GET_STATISTICS = kttc.getStatistics
elif PROVIDER == STAT_PROVIDER.NOOBMETER:
    GET_STATISTICS = noobmeter.getStatistics
else:
    assert False, "Stat provider is supported but not meant by the config initializer: %s" % PROVIDER
    

def _updatePlayerName(playerName, playerId):
    playerStat = GET_STATISTICS(REGION_SETTING, playerName, playerId)
    newName = playerStat + playerName
    _formatted[playerName] = newName


def formattedPlayerName(playerName):
    return _formatted.get(playerName, "[?]" + playerName)


def updatePlayerFormatByVehicleList(vehicles, forced=False):
    try:
        from threading import Thread

        vehicleInfoTasks = set()

        for vID, vData in vehicles.iteritems():
            if "name" in vData:
                playerName = vData["name"]

                if not forced and playerName in _formatted:
                    continue

                playerId = vData.get("accountDBID", PLAYER_ID_NOT_KNOWN)

                task = Thread(target=_updatePlayerName, args=(playerName, playerId))
                vehicleInfoTasks.add(task)
                task.start()

        logInfo("Vehicle info task count: %d" % len(vehicleInfoTasks))

        for task in vehicleInfoTasks:
            task.join()

        logInfo("Tasks are joined")
    except BaseException:
        logError("Can't update player format by vehicle list", traceback.format_exc())

    
def new_buildVehiclesData(self, vehicles):
    old_buildVehiclesData(self, vehicles)
    updatePlayerFormatByVehicleList(vehicles)
    

old_buildVehiclesData = ArenaDataProvider.buildVehiclesData
ArenaDataProvider.buildVehiclesData = new_buildVehiclesData


def new_player_format(self, vInfoVO, playerName=None):
    result = old_player_format(self, vInfoVO, playerName)
    playerName = formattedPlayerName(result.playerName)
    return PlayerFormatResult(result.playerFullName, playerName, result.clanAbbrev, result.regionCode, result.vehicleName)

old_player_format = PlayerFullNameFormatter.format
PlayerFullNameFormatter.format = new_player_format


print 'Load mod recent_stat by SerVB'
