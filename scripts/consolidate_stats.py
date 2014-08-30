__author__ = 'wittwerch'

from django.db.utils import IntegrityError

"""

DJANGO_SETTINGS_MODULE=settings
python consolidate_stats.py

GamePlayerStatus to consolidate
Season PK 21 1011   team.pk=2 => league 4
Season PK 22 1112   team.pk=2 => league 4

"""

import sys
sys.path.append('../src/')

from shcbelpa.models import *


season = Season.objects.get(pk=20)
team = Team.objects.get(pk=5)

for game_type in GameType.objects.all():
    for stat in SeasonPlayerStats.objects.getSeasonStats(season, team, game_type):
        stat.league = League.objects.get(name='Junioren B')
        print "%s %s %s %s %s" % (stat.season, stat.league, stat.game_type, stat.player, stat.points)
        try:
            stat.save()
        except IntegrityError:
            print stat.team
            print stat.player