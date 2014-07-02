from django.db import models
from django.utils.translation import ugettext_lazy as _
from mezzanine.blog.models import BlogPost

from .managers import GameManager

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

    def __unicode__(self):
        return "%s %s" % (self.first_name, self.last_name)

    class Meta:
        ordering = ['last_name']


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


class GameType(models.Model):
    name = models.CharField(max_length=20,unique=True)

    def __unicode__(self):
        return self.name

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

