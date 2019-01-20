from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from communications.utils import get_profile_data
from core.forms import SearchForm
from core.tasks import get_friends_status
from core.models import Platform
from players.models import Friend, Player


def index(request):
    players = Player.objects.all()
    friends = Friend.objects.all()
    platforms = Platform.objects.all()
    get_friends_status.delay()
    return render(request, 'core/index.html', {
        'players': players,
        'friends': friends,
        'platforms': platforms,
    })


def player_search(request):
    if not request.method == 'POST':
        return render(request, 'core/index.html')
    form = SearchForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        platform = form.cleaned_data['platforms']
        communication = get_profile_data(username, platform)
        if communication.error:
            messages.add_message(
                request,
                messages.ERROR,
                f'Usuário <strong>{username}</strong> não encontrado. '
                'Confira os dados ou selecione outra plataforma.'
            )
            return redirect(request.META.get('HTTP_REFERER'))
        return redirect('core:player-detail', username=communication.player_stats.player.username)


def player_detail(request, username):
    player = get_object_or_404(Player, username=username)
    platform = request.GET.get('platform')
    platforms = [platform.name for platform in player.platforms.all()]
    if platform not in platforms:
        platform = player.last_platform_name()
    status = player.statuses.filter(platform__name=platform).last()
    # get_match_history(player.uid)  # TODO: Refactor
    return render(request, 'core/player_detail.html', {
        'player': player,
        'status': status,
    })
