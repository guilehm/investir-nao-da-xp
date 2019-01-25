from django.core.cache import cache

from communications.models import Communication
from core.models import Platform
from players.models import Player


def get_profile_data(username, platform):
    cache_name = 'status-{platform}-{username}'.format(
        platform=platform.name,
        username=username,
    )
    has_data = cache.get(cache_name)
    if has_data:
        communication = Communication.objects.get(id=has_data)
    else:
        communication = Communication.objects.create(
            method='profile_data',
        )
        communication = communication.communicate(platform=platform.name, username=username)
        if not communication.error:
            communication.create_player_stats()
            cache.set(cache_name, communication.id)
    return communication


def get_match_history(account_id):
    communication = Communication.objects.create(
        method='match_history'
    )
    communication = communication.communicate(account_id=account_id)
    if not communication.error:
        communication.create_matches(account_id=account_id)
    return communication


def get_stats_by_season(user_id, user_clean_uid, platform_name, season):
    cache_name = 'status-by-season-{platform}-{season}-{user_clean_uid}'.format(
        platform=platform_name,
        season=season,
        user_clean_uid=user_clean_uid,
    )
    has_data = cache.get(cache_name)
    if has_data:
        communication = Communication.objects.get(id=has_data)
    else:
        communication = Communication.objects.create(
            method='stats_by_season'
        )
        communication = communication.communicate_gaming_sdk(
            user_uid=user_clean_uid,
            platform=platform_name,
            window=season,
        )
        if not communication.error:
            player = Player.objects.get(id=user_id)
            platform = Platform.objects.get(name=platform_name)
            communication.create_player_stats_by_season(
                player=player, platform=platform,
            )
            cache.set(cache_name, communication.id)
    return communication


def get_all_items():
    cache_name = 'get-all-items'
    has_data = cache.get(cache_name)
    if has_data:
        communication = Communication.objects.get(id=has_data)
    else:
        communication = Communication.objects.create(
            method='all_items'
        )
        communication = communication.communicate_get_items()
        cache.set(cache_name, communication.id, 20 * 60)
    return communication


def get_upcoming_items():
    cache_name = 'get-upcoming-items'
    has_data = cache.get(cache_name)
    if has_data:
        communication = Communication.objects.get(id=has_data)
    else:
        communication = Communication.objects.create(
            method='upcoming_items'
        )
        communication = communication.communicate_get_items()
        cache.set(cache_name, communication.id, 20 * 60)
    return communication
