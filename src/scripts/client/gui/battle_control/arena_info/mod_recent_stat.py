# coding=utf-8
# https://www.apache.org/licenses/LICENSE-2.0.html

REGION_SETTING = "ru"

_formatted = dict()  # {playerName: formattedPlayerName}
_PLAYER_ID_NOT_KNOWN = -1


def getSiteText(url):
    try:
        import urllib2
        html = urllib2.urlopen(url=url).read()
        return html
    except Exception as e:
        print "[---! The Recent Stat of You] Can't get site text. Reason: %s" % e
        return ""


def getPlayerId(idSiteText, nickname):
    try:
        nameTitle = "<h1>%s</h1>" % nickname
        nameTitleEndIndex = idSiteText.find(nameTitle) + len(nameTitle)
        idStartIndex = idSiteText.find("<!--", nameTitleEndIndex) + len("<!--")
        idEndIndex = idSiteText.find("-->", idStartIndex) - 1
        return int(idSiteText[idStartIndex:idEndIndex].strip())
    except Exception as e:
        print "[---! The Recent Stat of You] Can't get id from text. Reason: %s" % e
        return -1


def getNextRowCells(string, idx, td="td"):
    cellBegin = "<%s>" % td
    cellEnd = "</%s>" % td

    answer = list()
    rowEndIdx = string.find("</tr>", idx)
    nowTdIdx = string.find(cellBegin, idx)
    while nowTdIdx != -1 and nowTdIdx < rowEndIdx:
        nowTdBeginIdx = string.find(">", nowTdIdx) + 1
        nowTdEndIdx = string.find(cellEnd, nowTdIdx)

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


def getStatistics(region, nickname, playerId):
    traceback = None

    if playerId == _PLAYER_ID_NOT_KNOWN:
        idSiteText = getSiteText("http://www.noobmeter.com/player/%s/%s" % (region, nickname))
        playerId = getPlayerId(idSiteText, nickname)
        print "[--- The Recent Stat of You] Player ID of %s = %s" % (nickname, playerId)

    siteText = getSiteText("http://www.noobmeter.com/player/%s/%s/%d" % (region, nickname, playerId))
    siteText = siteText.replace("&nbsp;", " ").replace('"', "'")

    try:
        import traceback

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
        print "[--- The Recent Stat of You] Error in getStatistics(%s, %s, %s)" % (region, nickname, playerId)
        print traceback.format_exc()
        return "[?-?]"


def _updatePlayerName(playerName, playerId):
    playerStat = getStatistics(REGION_SETTING, playerName, playerId)
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

                playerId = vData.get("accountDBID", _PLAYER_ID_NOT_KNOWN)

                task = Thread(target=_updatePlayerName, args=(playerName, playerId))
                vehicleInfoTasks.add(task)
                task.start()

        print "[--- The Recent Stat of You] Vehicle info task count: %d" % len(vehicleInfoTasks)

        for task in vehicleInfoTasks:
            task.join()

        print "[--- The Recent Stat of You] Tasks are joined"
    except Exception as e:
        print "[---! The Recent Stat of You] Can't update player format by vehicle list. Reason: %s" % e
