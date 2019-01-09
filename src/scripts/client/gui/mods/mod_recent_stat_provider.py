# -*- coding: utf-8 -*-
# https://www.apache.org/licenses/LICENSE-2.0.html

from abc import ABCMeta, abstractmethod
import traceback

from mod_recent_stat_logging import logError


class StatProvider:
    __metaclass__ = ABCMeta

    name = "Abstract Stat Provider"

    def getStatistics(self, region, nickname, playerId, playerIdToData):
        # type: (str, str, int, dict) -> None
        try:
            self._getStatistics(region, nickname, playerId, playerIdToData)
        except BaseException:
            logError("Error in getStatistics(%s, %s, %s)" % (region, nickname, playerId), traceback.format_exc())

    @abstractmethod
    def _getStatistics(self, region, nickname, playerId, playerIdToData):
        # type: (str, str, int, dict) -> None
        pass
