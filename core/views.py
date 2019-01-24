from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from communications.utils import get_profile_data, get_stats_by_season
from core.forms import SearchForm
from core.models import Platform, Season
from core.tasks import get_friends_status
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
    window_name = request.GET.get('window') or 'alltime'
    try:
        window = Season.objects.get(name=window_name)
    except Season.DoesNotExist:
        window, _ = Season.objects.get_or_create(name='alltime')
    status = player.statuses.filter(
        platform__name=platform, window=window, source='fortnite_tracker'
    ).last()
    seasons = Season.objects.only_available()
    # get_match_history(player.uid)  # TODO: Refactor
    return render(request, 'core/player_detail.html', {
        'player': player,
        'status': status,  # FIXME: Refactor
        'seasons': seasons,
    })


def player_detail_by_season(request, username, season_number):
    player = get_object_or_404(Player, username=username)
    platform_name = player.last_platform_name()
    try:
        if season_number == 0:
            raise ValueError
        season_name = 'season{number}'.format(number=int(season_number))
    except ValueError:
        return redirect('core:player-detail', username=username)
    window, _ = Season.objects.get_or_create(name=season_name)
    stats = get_stats_by_season(player.id, player.clean_uid, platform_name, window)
    seasons = Season.objects.only_available()
    return render(request, 'core/player_detail_by_season.html', {
        'player': player,
        'status': stats,  # FIXME: Refactor
        'seasons': seasons
    })
