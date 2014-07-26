from django.contrib import admin

from .models import League, Club, Game, Team, Player, Season, GameRecap, Teaser

class LeagueAdmin(admin.ModelAdmin):
    pass
admin.site.register(League, LeagueAdmin)

class ClubAdmin(admin.ModelAdmin):
    pass
admin.site.register(Club, ClubAdmin)

class TeamAdmin(admin.ModelAdmin):
    pass
admin.site.register(Team, TeamAdmin)

class GameAdmin(admin.ModelAdmin):
    pass
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