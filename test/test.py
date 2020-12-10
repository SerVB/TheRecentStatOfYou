from os.path import dirname, abspath, join
import sys
import unittest


class RecentStatTests(unittest.TestCase):

    def test_players(self):
        from gui.mods.mod_recent_stat_loader import ModRecentStat
        modRecentStat = ModRecentStat()

        vehicleList = {
            1: {"name": "servbul007", "accountDBID": 971843},
            2: {"name": "GOLDaCTPEJI", "accountDBID": 11586077},

            1002: {"name": "bratt2222", "accountDBID": 22094837},
            1004: {"name": "andrew_274", "accountDBID": 38507088},
            1005: {"name": "petlik2013", "accountDBID": 62423382},
            1006: {"name": "ARGOFUS", "accountDBID": 18839045},
            1007: {"name": "mazdax700to", "accountDBID": 13463022},
            1008: {"name": "Monstr7s", "accountDBID": 27524379},
            1009: {"name": "booz1989", "accountDBID": 23372205},
            1010: {"name": "ROCKY2425", "accountDBID": 95885799},

            100500: {"name": "not_existing", "accountDBID": 100500100500},
            0: {"name": "anon", "accountDBID": 0},
        }

        modRecentStat.loadPlayerDataByVehicleList(vehicleList)

        for _, vehicle in vehicleList.items():
            accountId = vehicle["accountDBID"]
            name = vehicle["name"]

            formatted_name = modRecentStat.formatPlayerName(accountId, name)
            new_badge = modRecentStat.getPlayerBadgeIcon(accountId)

            if accountId == 0:
                self.assertEqual("? %s" % name, formatted_name)
                self.assertEqual(None, new_badge)
            else:
                splits = formatted_name.split()
                self.assertEqual(3, len(splits))

            print("%s, color: %s" % (
                modRecentStat.formatPlayerName(accountId, vehicle["name"]),
                modRecentStat.getPlayerBadgeIcon(accountId)
            ))


if __name__ == '__main__':
    source_root_relative_dir = "../src/scripts/client"
    this_script_dir = dirname(__file__)
    source_root_abs_dir = abspath(join(this_script_dir, source_root_relative_dir))

    if source_root_abs_dir not in sys.path:
        sys.path.append(source_root_abs_dir)

    unittest.main()
