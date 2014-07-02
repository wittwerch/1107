from django.db import models
from django.db.models import Q


class GameManager(models.Manager):

    def filter_by_team(self, team):
        # filter queryset by team where either home_team or away_team matches
        return super(GameManager, self).get_query_set().filter(Q(home_team=team) | Q(away_team=team))

