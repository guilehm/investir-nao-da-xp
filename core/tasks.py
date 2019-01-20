from __future__ import absolute_import, unicode_literals

import time

from celery import shared_task

from communications.utils import get_profile_data
from players.models import Friend


@shared_task
def add(x, y):
    return x + y


@shared_task
def get_friends_status():
    for friend in Friend.objects.all():
        player = friend.player
        get_profile_data(player.username, player.last_platform())
        time.sleep(2.1)
