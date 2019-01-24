from django.contrib import admin

from players.models import Friend, Matches, Player, PlayerStats


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('username', 'date_added')
    list_filter = ('date_added', 'platforms', 'seasons')
    search_fields = ('uid', 'username')
    readonly_fields = ('date_added', 'date_changed')


@admin.register(PlayerStats)
class PlayerStatsAdmin(admin.ModelAdmin):
    list_display = ('id', 'player', 'window', 'date_added')
    list_filter = ('player', 'date_added')
    search_fields = ('player__username', 'data')
    readonly_fields = ('date_added', 'date_changed')


@admin.register(Matches)
class MatchesAdmin(admin.ModelAdmin):
    list_display = ('id', 'player', 'date_added')
    list_filter = ('player', 'date_added')
    search_fields = ('player__username', 'data')
    readonly_fields = ('date_added', 'date_changed')


@admin.register(Friend)
class FriendAdmin(admin.ModelAdmin):
    list_display = ('id', 'player', 'date_added')
