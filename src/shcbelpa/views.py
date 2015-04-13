from collections import OrderedDict
import json

from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView, DetailView, ListView
from django.conf import settings
from cartridge.shop.models import Order
from mezzanine.blog.models import BlogPost
from mezzanine.utils.email import send_mail_template
from annoying.functions import get_object_or_None

from .models import Player, Team, GameType, Game, Season, SeasonPlayerStats, League, Album, Sponsor, Teaser, Table


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

        is_tournament_mode = False

        sections = {}
        for game_type in GameType.objects.all():
            # fetch games for this team, season and game_type
            games = Game.objects.filter_by_team(team).filter(season=season, game_type=game_type).order_by('date_time')
            # aggregate by date to find out if there are more than 1 game per day
            clustering = games.extra({'date':"date(date_time)"}).values('date').annotate(count=Count('id'))

            dates = OrderedDict()
            for day in clustering:
                dates[str(day['date'])] = []
                # if there are more than 1 game per day, it's a league which plays tournaments => different presentation
                if day['count'] > 1:
                    is_tournament_mode = True

            if is_tournament_mode:
                for game in games:
                    date = game.date_time.date()
                    # group games per day and then append it to the section
                    dates[str(date)].append(game)

                sections[game_type] = dates
            else:
                sections[game_type] = games

        context['is_tournament_mode'] = is_tournament_mode
        context['team'] = team
        context['current_season'] = season
        context['seasons'] = Game.objects.get_seasons(team)
        context['sections'] = sections

        # Table
        context['table'] = Table.objects.filter(season=season, league=team.league, game_type=game_type).order_by('position')

        return context


class GameView(DetailView):
    model = Game
    template_name = 'shcbelpa/game.html'
    context_object_name = 'game'


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

    def get_context_data(self, **kwargs):
        context = super(AlbumView, self).get_context_data(**kwargs)
        album = context['album']
        photos = []
        for photo in album.photos.all():
            photos.append({
                'thumb': photo.medium_url,
                'image': photo.content_url
            })

        context['json'] = json.dumps(photos)
        return context

class SponsorView(ListView):
    queryset = Sponsor.objects.all()
    template_name = 'shcbelpa/sponsor.html'
    context_object_name = "sponsors"


class OrderListView(TemplateView):
    """
    Display all order made in the shop by it's status
    """

    template_name = 'shcbelpa/shop/order_list.html'

    def get_context_data(self, **kwargs):
        context = super(OrderListView, self).get_context_data(**kwargs)

        # get all new order
        context['new_orders'] = Order.objects.filter(status=1).order_by('-time')

        # get all payed order
        context['payed_orders'] = Order.objects.filter(status=2).order_by('-time')

        return context


class OrderDetailView(DetailView):
    """
    Display an order with option to mark it as payed
    """

    model = Order
    template_name = 'shcbelpa/shop/order_detail.html'
    context_object_name = 'order'

    def post(self, request, *args, **kwargs):
        order = Order.objects.get(pk=kwargs['pk'])

        if order.status == 1:
            order.status = 2 # set to payed
            order.save()

            order_context = {"order": order, "request": request,
                             "order_items": order.items.all()}
            order_context.update(order.details_as_dict())

            receipt_template = "email/producer_notification"

            send_mail_template("Bestellung #%i" % order.id,
                           receipt_template, settings.SHOP_ORDER_FROM_EMAIL,
                           settings.SHOP_PRODUCER_EMAIL, context=order_context,
                           addr_bcc=settings.SHOP_ORDER_EMAIL_BCC or None, fail_silently=False)

        return redirect('order_detail', pk=order.pk)