# -*- coding: utf-8 -*-
# https://www.apache.org/licenses/LICENSE-2.0.html

from mod_recent_stat_constant import STAT_PROVIDER
from mod_recent_stat_logging import logError
from mod_recent_stat_provider_kttc import Kttc
from mod_recent_stat_provider_noobmeter import Noobmeter

REGION_SETTING = "ru"
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
