# -*- coding: utf-8 -*-
# https://www.apache.org/licenses/LICENSE-2.0.html

import traceback


def getSiteText(url):
    try:
        import urllib2
        html = urllib2.urlopen(url=url).read()
        return html
    except Exception as e:
        print "[---! The Recent Stat of You] Can't get site text. Reason: %s" % traceback.format_exc()
        return ""


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
