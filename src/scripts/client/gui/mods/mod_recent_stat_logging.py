# -*- coding: utf-8 -*-
# https://www.apache.org/licenses/LICENSE-2.0.html


def logInfo(message):
    # type: (str) -> None
    print "[--- The Recent Stat of You vvv]"
    print message
    print "[--- The Recent Stat of You ^^^]"


def logError(message, exceptionText):
    # type: (str, str) -> None
    print "[!--- The Recent Stat of You vvv]"
    print message
    print "[!--- Exception text:]"
    print exceptionText
    print "[!--- The Recent Stat of You ^^^]"
