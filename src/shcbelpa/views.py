from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, DetailView

from .models import Player, Team, GameType, Game, Season, SeasonPlayerStats


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

        sections = {}
        for game_type in GameType.objects.all():
            stats = SeasonPlayerStats.objects.filter(team=team, season=season, game_type=game_type)
            print stats
            sections[game_type] = stats

        context['sections'] = sections

        context['active'] = 'regular'
        if self.kwargs['game_type']:
            context['active'] = self.kwargs['game_type']

        return context
