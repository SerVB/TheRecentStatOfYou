# -*- coding: utf-8 -*-
# https://www.apache.org/licenses/LICENSE-2.0.html

import json
import traceback

from mod_recent_stat_constant import PLAYER_ID_NOT_KNOWN, STAT_FIELDS
from mod_recent_stat_logging import logInfo, logError
from mod_recent_stat_network import getRawSiteText, getFormattedHtmlText, getJsonText
from mod_recent_stat_provider import StatProvider


class Kttc(StatProvider):
    def _getStatistics(self, region, nickname, playerId, playerIdToData):
        # type: (str, str, int, dict) -> None
        playerData = playerIdToData[playerId]

        recentStatJson = json.loads(getJsonText("https://kttc.ru/wot/%s/user/%s/get-by-battles/%s/" % (region, nickname, playerId)))
        if recentStatJson["success"] and "1000" in recentStatJson["data"]:
            if recentStatJson["data"]["1000"]["BT"] != 0:  # Filter not valid recent stats
                playerData.wn8 = int(round(recentStatJson["data"]["1000"]["WN8"]))
                playerData.xwn8 = int(round(recentStatJson["data"]["1000"]["XVM"]))

                playerData.hasRecentStat = True
