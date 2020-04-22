# -*- coding: utf-8 -*-
# https://www.apache.org/licenses/LICENSE-2.0.html

PLAYER_ID_NOT_KNOWN = -1
COLUMN_ID_NOT_FOUND = -1
MAX_ITERATIONS = 1000


class STAT_PROVIDER(object):
    NOOBMETER = "noobmeter"
    KTTC = "kttc"

    SUPPORTED = frozenset((NOOBMETER, KTTC))


class STAT_FIELDS(object):
    WN8 = "wn8"
    XWN8 = "xwn8"
    BATTLES = "battles"
    KILO_BATTLES = "kb"


class CONFIG_MAIN(object):
    REGION = "region"
    TIMEOUT = "timeout"
    RECENT_STAT_PROVIDERS = "recentStatProviders"
    BADGE_TYPE = "badgeType"


class CONFIG_FORMAT(object):
    PLAYER_NAME = "playerName"
    NO_INFO = "noInfo"


class BADGE_TYPE(object):
    XWN8_COLOR = "xwn8Color"
    BOB2020_TEAM_COLOR = "bob2020TeamColor"
    # todo: add option to disable badges modification
