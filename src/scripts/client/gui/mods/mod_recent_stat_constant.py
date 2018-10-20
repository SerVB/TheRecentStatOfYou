# -*- coding: utf-8 -*-
# https://www.apache.org/licenses/LICENSE-2.0.html

PLAYER_ID_NOT_KNOWN = -1
COLUMN_ID_NOT_FOUND = -1
MAX_ITERATIONS = 1000


class STAT_PROVIDER(object):
    NOOBMETER = "noobmeter"
    KTTC = "kttc"

    SUPPORTED = (NOOBMETER, KTTC)


class STAT_FIELDS(object):
    RECENT_BATTLES = "recentBattles"
    RECENT_WN8 = "recentWn8"
    OVERALL_BATTLES = "overallBattles"
    OVERALL_WN8 = "overallWn8"
