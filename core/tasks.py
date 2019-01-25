from __future__ import absolute_import, unicode_literals

import time

import requests
from celery import shared_task

from communications.utils import get_all_items, get_profile_data, get_upcoming_items
from core.models import Item
from players.models import Friend


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
        'cost': data['cost'] if data.get('cost') != '???' else None,
        'type': data['type'] if data.get('type') else data['item'].get('type') if data.get('item') else '',
        'rarity': data['rarity'] if data.get('rarity') else data['item'].get('rarity') if data.get('item') else '',
        'captial': data['captial'] if data.get('captial') else data['item'].get('captial') if data.get('item') else '',
        'obtained_type': data['obtained_type'] if data.get(
            'obtained_type'
        ) else data['item'].get('obtained_type') if data.get('item') else '',
        'featured': data.get('featured'),
        'refundable': data.get('refundable'),
        'youtube': data.get('youtube'),
        'image': data['image'] if data.get('image') else data['item'].get('image') if data.get('item') else '',
        'image_transparent': data['images'].get(
            'transparent'
        ) if data.get('images') else data['item']['images']['transparent'],
        'image_background': data['images'].get(
            'background'
        ) if data.get('images') else data['item']['images']['background'],
        'image_information': data['images'].get(
            'info'
        ) if data.get('images') else data['item']['images']['information'],
        'ratings': data.get('ratings'),
        'last_update': data.get('lastupdate'),
    }
    return formatted_data


def create_item(data, is_upcoming=False):
    identifier = data['identifier'] if data.get('identifier') else data['itemid']
    item, _ = Item.objects.get_or_create(identifier=identifier)
    formatted_data = extract_item_data(data)
    for key, value in formatted_data.items():
        setattr(item, key, value)
    item.data = data
    if is_upcoming:
        item.is_upcoming = is_upcoming
    item.save()


@shared_task
def get_items():
    communication = get_all_items()
    if not communication.error:
        for item in communication.data:
            create_item(item)


@shared_task
def get_upcoming_items_task():
    communication = get_upcoming_items()

    if not communication.error:
        Item.objects.update(is_upcoming=False)
        for item in communication.data['items']:
            create_item(data=item, is_upcoming=True)
