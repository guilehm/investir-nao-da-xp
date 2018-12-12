from django import forms
from django.shortcuts import render

from communications.models import Communication
from core.forms import SearchForm
from core.models import Platform
from players.models import Player
from django.shortcuts import get_object_or_404


def index(request):
    players = Player.objects.all()
    platforms = Platform.objects.all()
    form = SearchForm()
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            platform = form.cleaned_data['platforms']
            communication = Communication.objects.create(
                method='profile_data',
            )
            communication = communication.communicate(platform=platform.name, username=username)
            if not communication.error:
                communication.create_player_stats()
    return render(request, 'core/index.html', {
        'players': players,
        'platforms': platforms,
        'form': form,
    })


def player_detail(request, username):
    player = get_object_or_404(Player, username=username)
    platform = request.GET.get('platform')
    platforms = [platform.name for platform in player.platforms.all()]
    if platform not in platforms:
        platform = player.last_platform()
    status = player.statuses.filter(platform__name=platform).last()
    return render(request, 'core/player_detail.html', {
        'player': player,
        'status': status,
    })
