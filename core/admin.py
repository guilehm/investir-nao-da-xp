from django.contrib import admin
from core.models import Player


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('username', 'date_added')
    list_filter = ('date_added', 'platforms')
    search_fields = ('uid', 'username')
