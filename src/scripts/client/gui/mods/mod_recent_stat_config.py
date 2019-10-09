# -*- coding: utf-8 -*-
# https://www.apache.org/licenses/LICENSE-2.0.html

from abc import ABCMeta
import traceback

from mod_recent_stat_logging import logError, logInfo


class Config:
    __metaclass__ = ABCMeta

    _defaultConfigPaths = ("no path",)

    def warnCantFindFiles(self):
        # type: () -> None
        logInfo("Can't open configs %s" % self._defaultConfigPaths)

    def warnNoAttribute(self, attributeName):
        # type: (str) -> None
        logInfo('No attribute "%s" in config "%s"' % (attributeName, self._defaultConfigPaths))

    def warnInvalidAttribute(self, attributeName, value, expectedValues):
        # type: (str, str, str) -> None
        logInfo('In config "%s": attribute "%s" has an invalid value "%s". Possible values: %s.' % (self._defaultConfigPaths, attributeName, value, expectedValues))
