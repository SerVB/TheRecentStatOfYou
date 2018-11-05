# -*- coding: utf-8 -*-
# https://www.apache.org/licenses/LICENSE-2.0.html

from abc import ABCMeta
import traceback

from mod_recent_stat_constant import STAT_PROVIDER
from mod_recent_stat_logging import logError, logInfo
from mod_recent_stat_provider_kttc import Kttc
from mod_recent_stat_provider_noobmeter import Noobmeter


class Config:
    __metaclass__ = ABCMeta

    _defaultConfigPath = "no path"

    def errorCantFindFile(self):
        # type: () -> None
        logError("Can't open config %s" % self._defaultConfigPath, traceback.format_exc())

    def warnNoAttribute(self, attributeName):
        # type: (str) -> None
        logInfo('No attribute "%s" in config "%s"' % (attributeName, self._defaultConfigPath))


PROVIDER_NAME = STAT_PROVIDER.KTTC

PROVIDER = None

if PROVIDER_NAME not in STAT_PROVIDER.SUPPORTED:
    assert False, "Stat provider isn't supported: %s" % PROVIDER_NAME
elif PROVIDER_NAME == STAT_PROVIDER.KTTC:
    PROVIDER = Kttc()
elif PROVIDER_NAME == STAT_PROVIDER.NOOBMETER:
    PROVIDER = Noobmeter()
else:
    logError("Stat provider is supported but not meant by the config initializer: %s" % PROVIDER_NAME, "")
