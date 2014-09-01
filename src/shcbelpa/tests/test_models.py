__author__ = 'wittwerch'

from datetime import datetime, timedelta
from django.test import TestCase

from shcbelpa.models import Season, Game, SeasonPlayerStats, GameType, Team, Player

class SeasonTestCase(TestCase):

    def setUp(self):
        pass

    def test_new_season(self):
        season = Season(start_date=datetime(2014,07,14), end_date=datetime(2015,07,15))
        # Save season that code property gets generated
        season.save()
        self.assertEqual(season.code, '1415')

    def test_current_season(self):
        now = datetime.now()
        start_date = now - timedelta(days=1)
        end_date = now + timedelta(days=365)

        Season(start_date=start_date, end_date=end_date).save()
        season = Season.objects.get_current_season()

        self.assertEqual(season.start_date.year, start_date.year)
        self.assertEqual(season.start_date.month, start_date.month)
        self.assertEqual(season.start_date.day, start_date.day)


class GameTestCase(TestCase):

    fixtures = [
        'shcbelpa.club.json',
        'shcbelpa.team.json',
        'shcbelpa.league.json',
        'shcbelpa.season.json',
        'shcbelpa.gametype.json',
        'shcbelpa.game.json'
    ]

    def test_date_time_of_existing_game(self):
        # NLA 1314 / 13.09.2013 against Kernenried
        game = Game.objects.get(pk=961)

        #from django.utils import timezone
        #date_time = timezone.make_aware(datetime(year=2013,month=9, day=13, hour=19, minute=30), timezone.get_default_timezone())
        date_time = datetime(year=2013,month=9, day=13, hour=19, minute=30)

        self.assertEqual(game.date_time, date_time)


class SeasonStatsTestCase(TestCase):

    fixtures = [
        'shcbelpa.club.json',
        'shcbelpa.team.json',
        'shcbelpa.league.json',
        'shcbelpa.season.json',
        'shcbelpa.gametype.json',
        'shcbelpa.player.json',
        'shcbelpa.seasonplayerstats.json'
    ]

    def test_legacy_stats(self):

        season = Season.objects.get(code='0708')
        team = Team.objects.get(pk=1)
        game_type = GameType.objects.get(name='Qualifikation')

        stats = SeasonPlayerStats.objects.get_season_stats_by_type(season, team, game_type)
        self.assertEqual(len(stats), 20)

        stat = stats[0]
        self.assertEqual(stat.player.pk, 231)
        self.assertEqual(stat.points, 52)


class TeamTestCase(TestCase):

    fixtures = [
        'shcbelpa.club.json',
        'shcbelpa.team.json',
        'shcbelpa.league.json'
    ]

    def test_team_code_property(self):
        blp = Team.objects.get(pk=1)
        self.assertEqual(blp.club.code, 'BLP')
        self.assertEqual(blp.code, 'BLP')

        blp2 = Team.objects.get(pk=2)
        self.assertEqual(blp2.club.code, 'BLP')
        self.assertEqual(blp2.code, 'BL2')

        juna = Team.objects.get(pk=3)
        self.assertEqual(juna.club.code, 'BLP')
        self.assertEqual(juna.code, 'BLP')







