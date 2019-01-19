from django.contrib import admin

from communications.models import Communication


@admin.register(Communication)
class CommunicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'method', 'error', 'date_added')
    list_filter = ('date_added', 'method')
    search_fields = ('id', 'data')
