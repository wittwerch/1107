from django.contrib import admin
from django.conf import settings

from .models import League, Club, Game, Team, Player, Season, GameRecap, Teaser, Roster, Sponsor
from django.contrib.admin import SimpleListFilter

class HomeTeamFilter(SimpleListFilter):

    title = 'Belper Mannschaft'

    parameter_name = 'team'

    def lookups(self, request, model_admin):
        values = []
        teams = Team.objects.filter(club__name=settings.HOME_CLUB)
        for team in teams:
            values.append((team.pk, team.get_level_display()))
        return values


    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset.all()
        else:
            return queryset.filter(team__pk=self.value())

class LeagueAdmin(admin.ModelAdmin):
    pass
admin.site.register(League, LeagueAdmin)

class ClubAdmin(admin.ModelAdmin):
    list_display = ('name', 'alias', 'code', 'city')
    search_fields = ['name', 'alias', 'code']
admin.site.register(Club, ClubAdmin)

class TeamAdmin(admin.ModelAdmin):
    list_display = ('club', 'level')
admin.site.register(Team, TeamAdmin)

class GameAdmin(admin.ModelAdmin):
    list_display = ['date_time', 'home_team', 'away_team', 'season', 'game_type']
    list_filter = ('league', 'season', 'game_type')
    ordering = ['-date_time']
admin.site.register(Game, GameAdmin)

class PlayerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'number')
    search_fields = ['first_name', 'last_name', 'number']
admin.site.register(Player, PlayerAdmin)

class SeasonAdmin(admin.ModelAdmin):
    pass
admin.site.register(Season, SeasonAdmin)

# Import admin fields layout from the mezzanine blog app
from mezzanine.blog.admin import blogpost_fieldsets
# add custom field game on top
blogpost_fieldsets[0][1]["fields"].insert(1, "game")

class GameRecapAdmin(admin.ModelAdmin):
    fieldsets = blogpost_fieldsets
admin.site.register(GameRecap, GameRecapAdmin)

class TeaserAdmin(admin.ModelAdmin):
    pass
admin.site.register(Teaser, TeaserAdmin)

class RosterAdmin(admin.ModelAdmin):
    list_display = ['team', 'player', 'position']
    list_filter = (HomeTeamFilter, 'position')
admin.site.register(Roster, RosterAdmin)

class SponsorAdmin(admin.ModelAdmin):
    pass
admin.site.register(Sponsor, SponsorAdmin)