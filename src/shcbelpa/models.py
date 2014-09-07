from datetime import date, datetime
from django.utils.timezone import now

from collections import OrderedDict
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.utils.encoding import smart_unicode
from django.core.urlresolvers import reverse

from sorl.thumbnail import ImageField

from mezzanine.blog.models import BlogPost

class League(models.Model):
    name = models.CharField(max_length=60)
    is_junior = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name


class Club(models.Model):
    name = models.CharField(max_length=60)
    # alternative name, used if a Club changes his name
    alias = models.CharField(max_length=60, blank=True)
    # Abbreviation for that club, used for the result box
    code = models.CharField(max_length=60, blank=False)
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

    photo = ImageField(upload_to='players', blank=True)

    def get_photo(self):
        try:
            return self.photo.path
        except ValueError:
            return "players/johndoe.jpg"

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

    @property
    def name(self):
        if self.level == '2':
            return "%s II" % self.club.name
        else:
            return self.club.name

    @property
    def code(self):
        if self.level.isdigit() and self.level != '1':
            return "%s%s" % (self.club.code[:2], self.level)
        return self.club.code

    def __unicode__(self):
        return "%s (%s)" % (self.club.name, self.get_level_display())


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
        try:
            return Season.objects.get(start_date__lte=date.today(),end_date__gte=date.today())
        except Season.DoesNotExist:
            if len(Season.objects.all()) > 0:
                # fallback to latest season
                return Season.objects.order_by('-start_date')[0]
            raise Exception("No season found!")


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

    def get_seasons(self, team):
        """
        Return seasons that have Games for that team
        """
        seasons = []
        for season in Season.objects.all().order_by('-start_date'):
            if len(Game.objects.filter(season=season).filter(Q(home_team=team) | Q(away_team=team))) > 0:
                seasons.append(season)
        return seasons

    def get_games_for_resultbox(self):

        season = Season.objects.get_current_season()
        resultbox = OrderedDict()

        for team in Team.objects.filter(club__name=settings.HOME_CLUB):
            last_game = None
            next_game = None
            # search last game
            games = Game.objects.filter(season=season, date_time__lte=datetime.now()).filter(Q(home_team=team) | Q(away_team=team)).order_by("-date_time")
            if len(games) > 0:
                last_game = games[0]

            games = Game.objects.filter(season=season, date_time__gte=datetime.now()).filter(Q(home_team=team) | Q(away_team=team)).order_by("date_time")
            if len(games) > 0:
                next_game = games[0]

            resultbox[team.league] = {
                'last_game': last_game,
                'next_game': next_game
            }

        return resultbox


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

    def opponent_team(self):
        if self.home_team.club.name == settings.HOME_CLUB:
            return self.away_team
        return self.home_team

    def is_home(self):
        if self.home_team.club.name == settings.HOME_CLUB:
            return True
        return False

    def get_absolute_url(self):
        """
        Return URL to GameRecap if available
        """
        try:
            return GameRecap.objects.get(game=self).get_absolute_url()
        except GameRecap.DoesNotExist:
            return None
        except GameRecap.MultipleObjectsReturned:
            # TODO: select by language
            return None


    def __unicode__(self):
        return smart_unicode("%s, %s - %s" % (self.date_time, self.home_team, self.away_team))

    class Meta:
        ordering = ['date_time']

    objects = GameManager()


class GameRecap(BlogPost):
    game = models.ForeignKey(Game)


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


    def get_hall_of_fame_stats(self):
        hall_of_fame_stats = []
        for player in Player.objects.all():
            stats_per_league = []
            for league in League.objects.filter(is_junior=False):
                stats = self.get_alltime_stats_by_player(player, league)
                stats_per_league.append(stats)
            stats = self._generate_stats(player, stats_per_league, from_dict=True)
            hall_of_fame_stats.append(stats)

        hall_of_fame_stats.sort(key=lambda x: x['points'], reverse=True)
        return hall_of_fame_stats


    def get_topscorer(self):
        topscorer = OrderedDict()
        season = Season.objects.get_current_season()
        for team in Team.objects.filter(club__name=settings.HOME_CLUB).order_by('pk'):
            stats = self.get_season_stats(season, team)
            if len(stats) > 0:
                topscorer[team.league] = stats[0]
        return topscorer


    def _generate_stats(self, player, season_player_stats, from_dict=False):
        stats = {}
        for field in ['gp', 'goal','assist','pm_2','pm_5','pm_10','pm_20','pm_25','pm','ppg','ppa','shg','sha', 'gw', 'gt']:
            if from_dict:
                values = (stat[field] for stat in season_player_stats)
            else:
                values = (stat.__dict__.get(field) for stat in season_player_stats)

            stats[field] = sum(values)

        stats['points'] = stats['goal'] + stats['assist']
        stats['points_avg'] = float(stats['points'])/float(stats['gp']) if stats['gp'] > 0 else 0
        stats['pm_avg'] = float(stats['pm'])/float(stats['gp']) if stats['gp'] > 0 else 0

        stats['player'] = player

        #stats['pm'] = sps.pm_2*2 + sps.pm_5*5 + sps.pm_10*10 + sps.pm_20*20 + sps.pm_25*25

        return stats


    def get_seasons(self, team):
        """
        Return seasons that have SeasonPlayerStats for that team
        """
        seasons = []
        for season in Season.objects.all().order_by('-start_date'):
            if len(SeasonPlayerStats.objects.filter(team=team, season=season)) > 0:
                seasons.append(season)
        return seasons

    #
    # def _accumulatedStats(self, stats):
    #     # generate temporary SeasonPlayerStats object which will hold the values, but never gets saved to the database
    #     sps = SeasonPlayerStats()
    #
    #
    #     len(stats)
    #     #print stats
    #     for (counter, field) in enumerate(['goal','assist','pm_2','pm_5','pm_10','pm_20','pm_25','ppg','ppa','shg','sha', 'gw', 'gt']):
    #         values = (stat.__dict__.get(field) for stat in stats)
    #         #print values
    #         sps.__dict__[field] = sum(values)
    #
    #     sps.pm = sps.pm_2*2 + sps.pm_5*5 + sps.pm_10*10 + sps.pm_20*20 + sps.pm_25*25
    #     sps.points = sps.goal + sps.assist
    #
    #     if isinstance(stats[0], GamePlayerStats):
    #         sps.gp = len(stats)
    #     else:
    #         sps.gp = sum((stat.__dict__.get("gp") for stat in stats))
    #
    #     return sps
    #
    # def _getSeasonStats(self, season, team, type, player):
    #     try:
    #         return SeasonPlayerStats.objects.get(season=season, team=team, game_type=type, player=player)
    #     except SeasonPlayerStats.DoesNotExist:
    #         stat = GamePlayerStats.objects.filter(game__season=season, game__game_type=type, player=player).filter(
    #             Q(game__home_team=team) | Q(game__away_team=team)
    #         )
    #
    #         if (len(stat)==0):
    #             return None
    #
    #         sps = self._accumulatedStats(stat)
    #         sps.player = player
    #         sps.team = team
    #         sps.season = season
    #         sps.game_type = type
    #         return sps
    #
    #
    # def getSeasonStats(self, season, team, type):
    #
    #     # ok, calculate stats out of gameplayerstats
    #     seasonStats = []
    #
    #     # get all player which played for this team in this season
    #     players = Player.objects.filter(
    #         Q(seasonplayerstats__team=team) & Q(seasonplayerstats__season=season) |
    #         Q(gameplayerstats__game__home_team=team) & Q(gameplayerstats__game__season=season) |
    #         Q(gameplayerstats__game__away_team=team) & Q(gameplayerstats__game__season=season)
    #     ).distinct()
    #
    #     for player in players:
    #         stat = self._getSeasonStats(season, team, type, player)
    #         if stat:
    #             seasonStats.append(stat)
    #
    #     seasonStats.sort(key=lambda x: x.points, reverse=True)
    #
    #     return seasonStats


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


class GamePlayerStats(CommonPlayerStats):
    game = models.ForeignKey(Game, limit_choices_to={'season': 1})

    class Meta:
        unique_together = (("player", "game"),)


class Photo(models.Model):

    gphoto_id = models.CharField(max_length=50, unique=True, db_index=True) # or big numeric field?
    owner = models.CharField(max_length=50)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True) # summary in api
    taken_date = models.DateTimeField()
    photopage_url = models.URLField()
    small_url = models.URLField()
    medium_url = models.URLField()
    thumbnail_url = models.URLField()
    content_url = models.URLField()
    geo_latitude = models.CharField(max_length=50, blank=True)
    geo_longitude = models.CharField(max_length=50, blank=True)
    updated = models.DateTimeField()

    #players = models.ManyToManyField(Player,related_name='photos',blank=True,null=True)

    def __unicode__(self):
        return u'%s' % self.title

    class Meta:
        ordering = ('-taken_date',)
        get_latest_by = 'taken_date'

class AlbumManager(models.Manager):

    def get_albums(self):
        queryset = super(AlbumManager, self).get_query_set()
        return queryset.exclude(title='Profilfotos').order_by('-updated')

class Album(models.Model):
    gphoto_id = models.CharField(max_length=50, unique=True, db_index=True) # or big numeric field?
    owner = models.CharField(max_length=50)	   # author in api
    albumname = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=512) # summary in api
    location = models.CharField(max_length=200)
    updated = models.DateTimeField()

    photos = models.ManyToManyField('Photo')

    game = models.ForeignKey(Game,blank=True,null=True)

    def numPhotos(self):
        return len(self.photos.objects.all())

    def __unicode__(self):
        return u"%s photo set by %s" % (self.title, self.owner)

    def numPhotos(self):
        return len(self.photos.all())

    class Meta:
        ordering = ('-updated',)

    objects = AlbumManager()

class Sponsor(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    url = models.URLField(blank=True, null=True)
    logo = ImageField(upload_to='sponsors', blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "Sponsor"
        verbose_name_plural = "Sponsoren"


class TeaserManager(models.Manager):

    def published(self):
        return self.filter(
            Q(publish_date__lte=now()) | Q(publish_date__isnull=True),
            Q(expiry_date__gte=now()) | Q(expiry_date__isnull=True))


class Teaser(models.Model):
    title = models.CharField(max_length=100)
    link = models.URLField(blank=True, null=True)
    image = ImageField(upload_to='teaser', blank=False)
    publish_date = models.DateTimeField()
    expiry_date = models.DateTimeField(blank=True, null=True)

    objects = TeaserManager()