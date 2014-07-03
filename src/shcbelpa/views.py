from collections import OrderedDict

from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, DetailView

from .models import Player, Team, GameType, Game, Season, SeasonPlayerStats, League


class HomeView(TemplateView):

    template_name = 'shcbelpa/homepage.html'


class SeasonView(TemplateView):

    template_name = 'shcbelpa/season.html'

    def get_context_data(self, **kwargs):
        context = super(SeasonView, self).get_context_data(**kwargs)

        team = get_object_or_404(Team, pk=self.kwargs['team_pk'])
        season = get_object_or_404(Season, code=self.kwargs['season'])

        sections = {}
        for game_type in GameType.objects.all():
            sections[game_type] = Game.objects.filter_by_team(team).filter(season=season, game_type=game_type)

        context['team'] = team
        context['season'] = season
        context['sections'] = sections

        return context

class PlayerView(DetailView):
    model = Player
    template_name = 'shcbelpa/player.html'
    context_object_name = 'player'

    def get_context_data(self, **kwargs):
        context = super(PlayerView, self).get_context_data(**kwargs)

        player = context['player']
        season = Season.objects.get_current_season()

        season_stats = []
        # get every team where player currently is on the roster (exclude coaches)
        for roster in player.roster_set.exclude(position='C'):
            stats =  SeasonPlayerStats.objects.get_season_stats_by_player(season, roster.team, player)
            season_stats.append([roster.team, stats])

        context['season_stats'] = season_stats

        alltime_stats = []
        # get every league the player ever played in (means has at least one SeasonPlayerStats entry)
        for league in League.objects.filter(seasonplayerstats__player=player).distinct().order_by('pk'):
            stats = SeasonPlayerStats.objects.get_alltime_stats_by_player(player, league)
            stats['league'] = league
            alltime_stats.append(stats)

        context['alltime_stats'] = alltime_stats
        context['season'] = season
        return context


class RosterView(TemplateView):

    template_name = 'shcbelpa/roster.html'

    def get_context_data(self, **kwargs):
        context = super(RosterView, self).get_context_data(**kwargs)

        team = get_object_or_404(Team, pk=self.kwargs['team_pk'])
        roster = (
            team.players.filter(roster__position='C'),
            team.players.filter(roster__position='G'),
            team.players.filter(roster__position='D'),
            team.players.filter(roster__position='O')
        )

        context['roster'] = roster
        context['team'] = team

        return context

class StatsView(TemplateView):

    template_name = 'shcbelpa/stats.html'

    def get_context_data(self, **kwargs):
        context = super(StatsView, self).get_context_data(**kwargs)

        season = get_object_or_404(Season, code=self.kwargs['season'])
        team = get_object_or_404(Team, pk=self.kwargs['team_pk'])

        sections = OrderedDict()
        sections['all'] = SeasonPlayerStats.objects.get_season_stats(season, team)

        for game_type in GameType.objects.all():
            stats = SeasonPlayerStats.objects.get_season_stats_by_type(season, team, game_type)
            sections[game_type.name] = stats

        context['sections'] = sections

        context['active'] = 'all'
        if self.kwargs['game_type']:
            context['active'] = self.kwargs['game_type']

        return context

