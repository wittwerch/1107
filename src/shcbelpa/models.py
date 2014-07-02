from datetime import date

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q, Sum
from django.contrib.staticfiles.templatetags.staticfiles import static

class League(models.Model):
    name = models.CharField(max_length=60)

    def __unicode__(self):
        return self.name


class Club(models.Model):
    name = models.CharField(max_length=60)
    # alternative name, used if a Club changes his name
    alias = models.CharField(max_length=60, blank=True)
    # city where the club plays
    city = models.CharField(max_length=60, blank=False)
    # URL to official website
    website = models.URLField(max_length=60, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "Club"
        verbose_name_plural = "Club"
        ordering = ['name']


class PlayerManager(models.Manager):

    def played_for_team(self, team, season):
        # filter queryset by team where either home_team or away_team matches
        return super(PlayerManager, self).get_query_set().filter(seasonplayerstats__team=team, seasonplayerstats__season=season).distinct()


class Player(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    number = models.DecimalField(max_digits=2, decimal_places=0,blank=True,null=True)
    born = models.DateField(blank=True,null=True)
    height = models.DecimalField(max_digits=3, decimal_places=0,blank=True,null=True)
    weight = models.DecimalField(max_digits=3, decimal_places=0,blank=True,null=True)

    SHOOTS_CHOICES = (
        ('L', _('Links')),
        ('R', _('Rechts')),
    )
    shoots = models.CharField(max_length=1,choices=SHOOTS_CHOICES,blank=True,null=True)

    photo = models.ImageField (
        upload_to='players',
        blank=True,
    )

    def photo_url(self):
        try:
            return self.photo.url
        except ValueError:
            return static("img/empty-profile.jpg")

    def __unicode__(self):
        return "%s %s" % (self.first_name, self.last_name)

    class Meta:
        ordering = ['last_name']

    objects = PlayerManager()

class Team(models.Model):

    club = models.ForeignKey(Club)

    LEVEL_CHOICES = (
        ('1', _('1. Mannschaft')),
        ('2', _('2. Mannschaft')),
        ('3', _('3. Mannschaft')),
        ('S', _('Senioren')),
        ('A', _('Junioren A')),
        ('B', _('Junioren B')),
        ('C', _('Junioren C')),
    )
    league = models.ForeignKey(League, blank=True,null=True)
    level = models.CharField(max_length=1,choices=LEVEL_CHOICES)
    players = models.ManyToManyField(Player, through='Roster',blank=True,null=True)

    def __unicode__(self):
        return self.club.name


class Roster(models.Model):
    team = models.ForeignKey(Team)
    player = models.ForeignKey(Player)

    POSITION_CHOICES = (
        ('C', 'Coaches'),
        ('G', 'Goalies'),
        ('D', 'Defensive'),
        ('O', 'Offensive'),
    )
    position = models.CharField(max_length=1,choices=POSITION_CHOICES)


class SeasonManager(models.Manager):

    def get_current_season(self):
        return Season.objects.get(start_date__lte=date.today(),end_date__gte=date.today())


class Season(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    code = models.CharField(max_length=4)

    # id from LigaManager
    lm_id = models.IntegerField(blank=True,null=True,unique=True)

    def save(self, *args, **kwargs):
        self.code = str(self.start_date.year)[2:] + str(self.end_date.year)[2:]
        super(Season, self).save(*args, **kwargs)

    def __unicode__(self):
        return "%s-%s" % (self.start_date.year, self.end_date.year)

    class Meta:
        ordering = ['-start_date']

    objects = SeasonManager()

class GameType(models.Model):
    name = models.CharField(max_length=20,unique=True)

    def __unicode__(self):
        return self.name

class GameManager(models.Manager):

    def filter_by_team(self, team):
        # filter queryset by team where either home_team or away_team matches
        return super(GameManager, self).get_query_set().filter(Q(home_team=team) | Q(away_team=team))


class Game(models.Model):
    date_time = models.DateTimeField()
    location = models.CharField(max_length=20,blank=True,null=True)
    # result, example: 10:5 (2:2, 5:3, 3:0)
    result = models.CharField(max_length=40,blank=True,null=True)

    season = models.ForeignKey(Season)
    league = models.ForeignKey(League)
    game_type = models.ForeignKey(GameType)

    home_team = models.ForeignKey(Team, related_name='home_team')
    away_team = models.ForeignKey(Team, related_name='away_team')

    # id from LigaManager
    lm_id = models.IntegerField(blank=True,null=True,unique=True)

    objects = GameManager()


class CommonPlayerStats(models.Model):
    player = models.ForeignKey(Player)

    goal = models.PositiveIntegerField(default=0)
    assist = models.PositiveIntegerField(default=0)
    pm_2 = models.PositiveIntegerField(default=0)
    pm_5 = models.PositiveIntegerField(default=0)
    pm_10 = models.PositiveIntegerField(default=0)
    pm_20 = models.PositiveIntegerField(default=0)
    pm_25 = models.PositiveIntegerField(default=0)
    ppg = models.PositiveIntegerField(default=0)
    ppa = models.PositiveIntegerField(default=0)
    shg = models.PositiveIntegerField(default=0)
    sha = models.PositiveIntegerField(default=0)
    gw = models.PositiveIntegerField(default=0)
    gt = models.PositiveIntegerField(default=0)

    class Meta:
        abstract = True


class SeasonPlayerStatsManager(models.Manager):

    def get_season_stats_by_type(self, season, team, game_type):
        queryset = super(SeasonPlayerStatsManager, self).get_query_set().filter(season=season, team=team, game_type=game_type)
        return queryset.filter(season=season, team=team, game_type=game_type)

    def get_season_stats(self, season, team):
        players = Player.objects.played_for_team(team, season)
        stats = []
        for player in players:
            season_player_stats = super(SeasonPlayerStatsManager, self).get_query_set().filter(season=season, team=team, player=player)
            stat = self._generate_stats(player, season_player_stats)
            stats.append(stat)

        stats.sort(key=lambda x: x['points'], reverse=True)

        return stats

    def get_season_stats_by_player(self, season, team, player):
        season_player_stats = super(SeasonPlayerStatsManager, self).get_query_set().filter(season=season, team=team, player=player)
        stat = self._generate_stats(player, season_player_stats)
        return stat


    def get_alltime_stats_by_player(self, player, league):
        season_player_stats = super(SeasonPlayerStatsManager, self).get_query_set().filter(player=player, league=league)
        stats = self._generate_stats(player, season_player_stats)
        return stats


    def _generate_stats(self, player, season_player_stats):
        stats = {}
        for field in ['gp', 'goal','assist','pm_2','pm_5','pm_10','pm_20','pm_25','pm','ppg','ppa','shg','sha', 'gw', 'gt']:
            values = (stat.__dict__.get(field) for stat in season_player_stats)
            stats[field] = sum(values)

        stats['points'] = stats['goal'] + stats['assist']
        stats['points_avg'] = float(stats['points'])/float(stats['gp']) if stats['gp'] > 0 else 0
        stats['pm_avg'] = float(stats['pm'])/float(stats['gp']) if stats['gp'] > 0 else 0

        stats['player'] = player

        #stats['pm'] = sps.pm_2*2 + sps.pm_5*5 + sps.pm_10*10 + sps.pm_20*20 + sps.pm_25*25

        return stats


class SeasonPlayerStats(CommonPlayerStats):
    gp = models.PositiveIntegerField(default=0)
    points = models.PositiveIntegerField(default=0)
    pm = models.PositiveIntegerField(default=0)

    team = models.ForeignKey(Team)
    season = models.ForeignKey(Season)
    game_type = models.ForeignKey(GameType)
    league = models.ForeignKey(League)


    @property
    def points_avg(self):
        if self.gp > 0:
            return float(self.points)/float(self.gp)
        return 0

    @property
    def pm_avg(self):
        if self.gp > 0:
            return float(self.pm)/float(self.gp)
        return 0


    class Meta:
        unique_together = (("player", "season", "game_type", "team", "league"),)

        ordering = ['-points']

    objects = SeasonPlayerStatsManager()


