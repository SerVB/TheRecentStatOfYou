# -*- coding: utf-8 -*-
# https://www.apache.org/licenses/LICENSE-2.0.html

import random
from urllib2 import urlopen, Request

from mod_recent_stat_string import removeTags

_DEFAULT_TIMEOUT = 10


def generateUserAgent():
    # type: () -> str
    firefox = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:{0}.0) Gecko/20100101 Firefox/{0}.0"
    firefoxVersion = random.randint(61, 62)
    userAgent = firefox.format(firefoxVersion)
    return userAgent


def generateHeaders():
    # type: () -> dict
    headers = {"User-Agent": generateUserAgent()}
    return headers


def getRawSiteText(url, timeout=_DEFAULT_TIMEOUT):
    # type: (str, int) -> str
    req = Request(url, headers=generateHeaders())
    html = urlopen(req, timeout=timeout).read()
    return html


def getFormattedHtmlText(url, timeout=_DEFAULT_TIMEOUT):
    # type: (str, int) -> str
    return getRawSiteText(url, timeout).replace("&nbsp;", " ").replace('"', "'")


def getJsonText(url, timeout=_DEFAULT_TIMEOUT):
    # type: (str, int) -> str
    return getRawSiteText(url, timeout).replace("'", '"')


def getNextRowCells(string, idx, td="td"):
    # type: (str, int, str) -> list
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


# Returns str of number in <td>...</td> or None if not found
def getNumberFromCell(tdText):
    # type: (str) -> [None, str]
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
