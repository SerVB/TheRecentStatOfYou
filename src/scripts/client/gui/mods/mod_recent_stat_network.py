# -*- coding: utf-8 -*-
# https://www.apache.org/licenses/LICENSE-2.0.html


def getRawSiteText(url):
    import urllib2
    html = urllib2.urlopen(url=url).read().replace("&nbsp;", " ").replace('"', "'")
    return html


def getFormattedHtmlText(url):
    return getRawSiteText(url).replace("&nbsp;", " ").replace('"', "'")


def getJsonText(url):
    return getRawSiteText(url).replace("'", '"')


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
