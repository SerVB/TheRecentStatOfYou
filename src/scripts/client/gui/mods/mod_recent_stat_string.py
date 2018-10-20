# -*- coding: utf-8 -*-
# https://www.apache.org/licenses/LICENSE-2.0.html


def removeSubstringsByBeginAndEnd(string, begin, end):
    answer = ""

    nextStart = 0

    while nextStart < len(string):
        beginIdx = string.find(begin, nextStart)
        if beginIdx == -1:
            answer += string[nextStart:]
            return answer
        else:
            answer += string[nextStart:beginIdx]

        endIdx = string.find(end, beginIdx + 1)
        if endIdx == -1:
            return answer

        nextStart = endIdx + len(end)

    return answer


def removeTags(text):
    return removeSubstringsByBeginAndEnd(text, "<", ">")
