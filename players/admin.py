from django.contrib import admin

from players.models import Player, PlayerStats


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('username', 'date_added')
    list_filter = ('date_added', 'platforms')
    search_fields = ('uid', 'username')


@admin.register(PlayerStats)
class PlayerStatsAdmin(admin.ModelAdmin):
    list_display = ('player', 'date_added')
    list_filter = ('player', 'date_added')
    search_fields = ('player__username', 'data')
