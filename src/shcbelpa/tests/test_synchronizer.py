from django.test import TestCase

from shcbelpa.synchronizer import LigaManager

class LigaManagerSynchronizerTest(TestCase):

    fixtures = ['shcbelpa.club.json', 'shcbelpa.team.json', 'shcbelpa.league.json']

    def setUp(self):
        self.lm = LigaManager()

    def test_get_team_with_fanion_team(self):
        team = self.lm._get_team("SHC Belpa 1107")
        self.assertEqual(team.club.name, 'SHC Belpa 1107')
        self.assertEqual(team.level, '1')

        team = self.lm._get_team("SHC Belpa 1107 2")
        self.assertEqual(team.club.name, 'SHC Belpa 1107')
        self.assertEqual(team.level, '2')

        team = self.lm._get_team("SHC Belpa 1107 3")
        self.assertEqual(team.club.name, 'SHC Belpa 1107')
        self.assertEqual(team.level, '3')

    def test_get_team_with_latin_letter(self):
        team = self.lm._get_team("SHC Belpa 1107 II")
        self.assertEqual(team.club.name, 'SHC Belpa 1107')
        self.assertEqual(team.level, '2')

    def test_get_team_with_junioren(self):
        team = self.lm._get_team("SHC Belpa 1107 JA")
        self.assertEqual(team.club.name, 'SHC Belpa 1107')
        self.assertEqual(team.level, 'A')

        team = self.lm._get_team("SHC Belpa 1107 JB")
        self.assertEqual(team.club.name, 'SHC Belpa 1107')
        self.assertEqual(team.level, 'B')

        team = self.lm._get_team("SHC Belpa 1107 JC")
        self.assertEqual(team.club.name, 'SHC Belpa 1107')
        self.assertEqual(team.level, 'C')

    def test_get_team_with_forced_level(self):
        forced_level = 'A'
        team = self.lm._get_team("SHC Belpa 1107", forced_level)
        self.assertEqual(team.club.name, 'SHC Belpa 1107')
        self.assertEqual(team.level, 'A')
