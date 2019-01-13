# -*- coding: utf-8 -*-
# https://www.apache.org/licenses/LICENSE-2.0.html

from mod_recent_stat_config_format import ConfigFormat
from mod_recent_stat_constant import STAT_FIELDS


class PlayerData(object):
    battles = None  # type: [int, None]
    kb = None  # type: [int, None]
    wn8 = None  # type: [int, None]
    xwn8 = None  # type: [int, None]

    hasRecentStat = False  # type: bool

    def createDict(self, configFormat):
        # type: (ConfigFormat) -> dict
        return {
            STAT_FIELDS.KILO_BATTLES: self.orNoInfo(self.kb, configFormat),
            STAT_FIELDS.BATTLES: self.orNoInfo(self.battles, configFormat),
            STAT_FIELDS.WN8: self.orNoInfo(self.wn8, configFormat),
            STAT_FIELDS.XWN8: self.orNoInfo(self.xwn8, configFormat),
        }

    @staticmethod
    def orNoInfo(value, configFormat):
        # type: ([int, None], ConfigFormat) -> [int, str]
        if value is None:
            return configFormat.noInfo
        return value
