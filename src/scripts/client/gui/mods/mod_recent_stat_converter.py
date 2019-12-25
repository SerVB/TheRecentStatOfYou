# -*- coding: utf-8 -*-
# https://www.apache.org/licenses/LICENSE-2.0.html


def formatBattlesToKiloBattles(battles):
    # type: ([str, int, float]) -> int
    return int(round(int(battles) / 1000.0))


def getXWN8(wn8):
    # type: (float) -> int
    return int(round(max(0.0, min(99.0, wn8*(wn8*(wn8*(wn8*(wn8*(-wn8*0.00000000000000000009762 + 0.0000000000000016221) - 0.00000000001007) + 0.000000027916) - 0.000036982) + 0.05577) - 1.3))))


def isPlayerFake(accountDBID):
    # type: (int) -> bool
    return accountDBID == 0
