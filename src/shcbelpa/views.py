from collections import OrderedDict

from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, DetailView, ListView
from mezzanine.blog.models import BlogPost

from .models import Player, Team, GameType, Game, Season, SeasonPlayerStats, League, Album, Sponsor, Teaser


class HomeView(TemplateView):

    template_name = 'shcbelpa/homepage.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['blog_posts'] = BlogPost.objects.published()[:10]
        context['teasers'] = Teaser.objects.published()
        context['resultbox'] = Game.objects.get_games_for_resultbox()
        context['topscorer'] = SeasonPlayerStats.objects.get_topscorer()
        return context

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
        context['current_season'] = season
        context['seasons'] = Game.objects.get_seasons(team)
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
            ('coach', team.players.filter(roster__position='C')),
            ('goalie', team.players.filter(roster__position='G')),
            ('defense', team.players.filter(roster__position='D')),
            ('offense', team.players.filter(roster__position='O'))
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

        context['team'] = team
        context['current_season'] = season
        context['seasons'] = SeasonPlayerStats.objects.get_seasons(team)

        sections = OrderedDict()
        sections['Total'] = SeasonPlayerStats.objects.get_season_stats(season, team)

        for game_type in GameType.objects.all().order_by('pk'):
            stats = SeasonPlayerStats.objects.get_season_stats_by_type(season, team, game_type)
            sections[game_type.name] = stats

        context['sections'] = sections

        return context


class HallOfFameView(TemplateView):

    template_name = 'shcbelpa/hall-of-fame.html'

    def get_context_data(self, **kwargs):
        context = super(HallOfFameView, self).get_context_data(**kwargs)
        stats = SeasonPlayerStats.objects.get_hall_of_fame_stats()

        stats.sort(key=lambda x: x['points'], reverse=True)
        context['best_scorer'] = stats[:3]

        stats.sort(key=lambda x: x['gp'], reverse=True)
        context['most_games'] = stats[:3]

        stats.sort(key=lambda x: x['pm'], reverse=True)
        context['most_penalties'] = stats[:3]

        return context


class GalleryView(ListView):
    queryset = Album.objects.all().order_by('-updated')
    template_name = 'shcbelpa/gallery.html'
    paginate_by = 16


class AlbumView(DetailView):
    model = Album
    context_object_name = 'album'
    template_name = 'shcbelpa/album.html'


class SponsorView(ListView):
    queryset = Sponsor.objects.all()
    template_name = 'shcbelpa/sponsor.html'
    context_object_name = "sponsors"