from __future__ import absolute_import, unicode_literals

import time
import requests
from celery import shared_task
from communications.utils import get_profile_data, get_all_items
from players.models import Friend
from core.models import Item


@shared_task
def add(x, y):
    return x + y


@shared_task
def get_friends_status():
    for friend in Friend.objects.all():
        player = friend.player
        get_profile_data(player.username, player.last_platform())
        time.sleep(2.5)


@shared_task
def assure_user_id_at_api_database(username):
    url = f'https://fortnite-public-api.theapinetwork.com/prod09/users/id?username={username}'
    requests.get(url)


def extract_item_data(data):
    formatted_data = {
        'name': data.get('name'),
        'description': data.get('description'),
        'upcoming': data.get('upcoming'),
        'cost': data.get('cost'),
        'type': data.get('type'),
        'rarity': data.get('rarity'),
        'image': data.get('image'),
        'captial': data.get('captial'),
        'obtained_type': data.get('obtained_type'),
        'featured': data.get('featured'),
        'refundable': data.get('refundable'),
        'youtube': data.get('youtube'),
        'image_transparent': data['images'].get('transparent'),
        'image_background': data['images'].get('background'),
        'image_information': data['images'].get('info'),
        'ratings': data.get('ratings'),
        'last_update': data.get('lastupdate'),
    }
    return formatted_data


@shared_task
def create_item(data):
    item, _ = Item.objects.get_or_create(identifier=data.get('identifier'))
    formatted_data = extract_item_data(data)
    for key, value in formatted_data.items():
        setattr(item, key, value)
    item.save()


@shared_task
def get_items():
    communication = get_all_items()
    if not communication.error:
        for item in communication.data:
            create_item.delay(item)
