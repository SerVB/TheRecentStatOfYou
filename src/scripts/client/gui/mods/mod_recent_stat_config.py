# -*- coding: utf-8 -*-
# https://www.apache.org/licenses/LICENSE-2.0.html

from mod_recent_stat_constant import STAT_PROVIDER
import mod_recent_stat_provider_kttc
import mod_recent_stat_provider_noobmeter

REGION_SETTING = "ru"
PROVIDER = STAT_PROVIDER.KTTC
GET_STATISTICS = None

if PROVIDER not in STAT_PROVIDER.SUPPORTED:
    assert False, "Stat provider isn't supported: %s" % PROVIDER
elif PROVIDER == STAT_PROVIDER.KTTC:
    GET_STATISTICS = mod_recent_stat_provider_kttc.getStatistics
elif PROVIDER == STAT_PROVIDER.NOOBMETER:
    GET_STATISTICS = mod_recent_stat_provider_noobmeter.getStatistics
else:
    assert False, "Stat provider is supported but not meant by the config initializer: %s" % PROVIDER
