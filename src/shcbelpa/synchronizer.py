import re
from datetime import datetime
import json
import requests
import urllib
import logging
import untangle
from django.conf import settings
from django.db.models import Q
import pytz
from annoying.functions import get_object_or_None

from .models import Team, GameType, League, Game, Season, Club, Player, SeasonPlayerStats, Table


class LigaManagerError(Exception):
    pass


class LigaManager:

    _logger = logging.getLogger(__name__)

    WS_URL = "http://liga.ssha.ch/xml"
    MAPPING_FILE = "%s/shcbelpa/mapping.json" % settings.PROJECT_ROOT

    def __init__(self):
        # load data mapping from file
        with open(self.MAPPING_FILE) as data_file:
            self._mapping = json.load(data_file)

    def _call_webservice(self, url, params):
        _url = "%s?%s" % (url, urllib.urlencode(params))

        self._logger.debug("Calling webservice %s" % _url)
        response = requests.get(_url)

        if response.status_code >= 500:
            raise LigaManagerError("Webservice at {} returned a http error {}".format(_url, response.status_code))

        return response

    def _get_player(self, surname, lastname):
        try:
            return Player.objects.get(first_name=surname, last_name=lastname)
        except Player.MultipleObjectsReturned:
            self._logger.error("Multiple Player found for %s %s" % (surname, lastname))
        except Player.DoesNotExist:
            self._logger.error("Player %s %s not found!" % (surname, lastname))
            return None

    def sync_stats(self, team, league, game_type, league_ssha_id):
        url = "%s/scorerliste.aspx" % self.WS_URL
        params = {
            "typ": "liga",
            "id": league_ssha_id
        }
        response = self._call_webservice(url, params)
        season = Season.objects.get(lm_id=self._mapping['season_id'])
        xml_stats = {}
        try:
            xml_stats = untangle.parse(response.content).ihs.Spieler
        except IndexError:
            self._logger.info("No stats found")

        for xml in xml_stats:

            if xml.vereinshort.cdata != 'BLP':
                continue

            player = self._get_player(xml.vorname.cdata, xml.nachname.cdata)
            if player is None:
                continue

            filter = {
                'player': player,
                'season': season,
                'team': team,
                'league': league,
                'game_type': game_type
            }
            try:
                stat = SeasonPlayerStats.objects.get(**filter)
            except SeasonPlayerStats.DoesNotExist:
                stat = SeasonPlayerStats(**filter)

            stat.gp = xml.anzahlspiele.cdata
            stat.points = xml.totalpkt.cdata
            stat.goal = xml.totaltore.cdata
            stat.assist = int(xml.totalass1.cdata) + int(xml.totalass2.cdata)

            stat.save()

    def sync_penalties(self, team, league, game_type, league_ssha_id):
        url = "%s/strafenliste.aspx" % self.WS_URL
        params = {
            "typ": "liga",
            "id": league_ssha_id
        }
        response = self._call_webservice(url, params)
        season = Season.objects.get(lm_id=self._mapping['season_id'])
        xml_stats = {}
        try:
            xml_stats = untangle.parse(response.content).ihs.Spieler
        except IndexError:
            self._logger.info("No penalties found")

        for xml in xml_stats:

            if xml.vereinshort.cdata != 'BLP':
                continue

            player = self._get_player(xml.vorname.cdata, xml.nachname.cdata)
            if player is None:
                continue

            filter = {
                'player': player,
                'season': season,
                'team': team,
                'league': league,
                'game_type': game_type
            }
            try:
                stat = SeasonPlayerStats.objects.get(**filter)
            except SeasonPlayerStats.DoesNotExist:
                stat = SeasonPlayerStats(**filter)

            stat.pm = xml.totalstrafen.cdata

            stat.save()

    def _get_team(self, string, force_level=None):
        #locale.setlocale(locale.LC_ALL, 'de_DE')
        pattern = re.compile('((?u)[\w\- ]*) J?([1-9ABCI]*)$')

        self._logger.debug("Matching %s" % string)
        match = pattern.match(string)

        if match:
            club_name = match.group(1)
            level = match.group(2)
            if level == 'II':
                level = 2
        else:
            club_name = string
            level = 1

        if force_level:
            level = force_level

        self._logger.debug("Search club '%s'" % club_name)
        club = Club.objects.get(Q(name=club_name) | Q(alias=club_name))
        self._logger.debug("Search team with level '%s'" % level)
        return Team.objects.get(club=club, level=level)

    def sync_table(self, season, league, league_ssha_id, game_type):
        url = "%s/tabelle.aspx" % self.WS_URL
        params = {
            "typ": "liga",
            "id": league_ssha_id
        }
        self._logger.info("Fetching table for league %s" % (league_ssha_id, ))
        response = self._call_webservice(url, params)

        xml_table = untangle.parse(response.content)

        try:
            for xml in xml_table.ihs.Mannschaften.Mannschaft:
                team = self._get_team(xml.Team.cdata)
                table = get_object_or_None(Table, team=team, season=season, league=league, game_type=game_type)
                if table is None:
                    table = Table(team=team, season=season, league=league, game_type=game_type)
                table.position = int(xml.Rang.cdata)
                table.gp = int(xml.Spiele.cdata)
                table.win = int(xml.Siege.cdata)
                table.loss = int(xml.Niederlagen.cdata)
                table.tie = int(xml.Remis.cdata)
                table.diff = xml.Tore.cdata
                table.points = int(xml.Punkte.cdata)

                table.save()
        except IndexError:
            self._logger.debug("No table entries found!")

    def sync_game(self, xml, team, league, type):
        spielnr = int(xml.spielnr.cdata)
        season = Season.objects.get(lm_id=self._mapping['season_id'])

        naive = datetime.strptime(xml.datum.cdata, "%d.%m.%Y %H:%M:%S")
        date_time = pytz.timezone(settings.TIME_ZONE).localize(naive, is_dst=None)

        try:
            game = Game.objects.get(season=season, league=league, game_type=type, date_time=date_time)
            print game
            if game.lm_id and game.lm_id != spielnr:
                raise Exception("Inconsistent data! Game found: pk=%i, lm_id=%i but spielnr=%i" % (game.pk, game.lm_id, spielnr))
        except Game.DoesNotExist:
            game = Game(season=season, league=league, game_type=type)
            game.date_time = date_time

        game.lm_id = spielnr
        game.location = xml.spielort.cdata

        force_level = None
        if team.level in ('A', 'B', 'C'):
            force_level = team.level

        game.home_team = self._get_team(xml.heim.cdata, force_level)
        game.away_team = self._get_team(xml.gast.cdata, force_level)

        game.result = xml.resultat.cdata

        game.save()

    def sync_games(self):

        url = "%s/spielplan.aspx" % self.WS_URL

        for team_pk in self._mapping['teams']:
            try:
                team = Team.objects.get(pk=team_pk)
            except:
                print team_pk
                raise

            team_lm_id = self._mapping['teams'][team_pk]['team_id']
            league = League.objects.get(pk=self._mapping['teams'][team_pk]['league_id'])

            for type_pk, league_lm_id in self._mapping['teams'][team_pk]['map'].iteritems():
                type = GameType.objects.get(pk=type_pk)
                params = {
                    "typ": "team",
                    "list": "all",
                    "id": team_lm_id,
                    "ligaid": league_lm_id
                }
                self._logger.info("Fetching games for team %s" % (team, ))
                response = self._call_webservice(url, params)
                xml_games = untangle.parse(response.content)

                try:
                    for xml in xml_games.ihs.Spiel:
                        self.sync_game(xml, team, league, type)
                except IndexError:
                    self._logger.debug("No games found!")

                # TODO: Don't import Cup stats, because they are wrong
                if type.id != 5:
                    self.sync_stats(team, league, type, league_lm_id)
                    self.sync_penalties(team, league, type, league_lm_id)

                if type.id == 2:
                    season = Season.objects.get(lm_id=self._mapping['season_id'])
                    self.sync_table(season, league, league_lm_id, type)