# -*- coding: utf-8 -*-
# https://www.apache.org/licenses/LICENSE-2.0.html

from mod_recent_stat_constant import STAT_FIELDS


class PlayerData(object):
    battles = None  # type: [int, None]
    kb = None  # type: [int, None]
    wn8 = None  # type: [int, None]
    xwn8 = None  # type: [int, None]

    hasRecentStat = False  # type: bool

    def createDict(self):
        # type: () -> dict
        return {
            STAT_FIELDS.KILO_BATTLES: self.kb,
            STAT_FIELDS.BATTLES: self.battles,
            STAT_FIELDS.WN8: self.wn8,
            STAT_FIELDS.XWN8: self.xwn8,
        }
