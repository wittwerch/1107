from django.contrib import admin

from .models import League, Club, Game, Team, Player, Season, GameRecap, Teaser, Roster, Sponsor

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

class GameRecapAdmin(admin.ModelAdmin):
    pass
admin.site.register(GameRecap, GameRecapAdmin)

class TeaserAdmin(admin.ModelAdmin):
    pass
admin.site.register(Teaser, TeaserAdmin)

class RosterAdmin(admin.ModelAdmin):
    list_display = ['team', 'player', 'position']
    list_filter = ('team', 'position')
admin.site.register(Roster, RosterAdmin)

class SponsorAdmin(admin.ModelAdmin):
    pass
admin.site.register(Sponsor, SponsorAdmin)