# -*- coding: utf-8 -*-
# https://www.apache.org/licenses/LICENSE-2.0.html


def formatBattlesToKiloBattles(battles):
    # type: ([str, int, float]) -> str
    return str(int(round(int(battles) / 1000.0)))


def getXWN8(wn8):
    # type: (float) -> [str, int]
    return 'XX' if wn8 > 3800 else int(round(max(0.0, min(100.0, wn8*(wn8*(wn8*(wn8*(wn8*(-wn8*0.00000000000000000009762 + 0.0000000000000016221) - 0.00000000001007) + 0.000000027916) - 0.000036982) + 0.05577) - 1.3))))
