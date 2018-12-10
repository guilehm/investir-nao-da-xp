from django.contrib import admin

from communications.models import Communication


@admin.register(Communication)
class CommunicationAdmin(admin.ModelAdmin):
    list_display = ('id',)
    list_filter = ('date_added',)
    search_fields = ('id', 'data')
