from django.contrib import admin

from core.models import Platform, Season


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_long', 'date_added')
    list_filter = ('date_added', 'date_changed')
    search_fields = ('name',)


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_added')
    list_filter = ('date_added', 'date_changed')
    search_fields = ('name',)
