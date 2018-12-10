from django.contrib.postgres.fields import JSONField
from django.db import models

from communications.models import Communication


class Player(models.Model):
    uid = models.CharField(max_length=100, unique=True, db_index=True, null=True, blank=True)
    username = models.CharField(max_length=50, unique=True)
    platforms = models.CharField(max_length=100, null=True, blank=True)
    seasons = models.CharField(max_length=100, null=True, blank=True)

    date_added = models.DateTimeField(auto_now_add=True)
    date_changed = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.username}'

    def get_user_data(self):
        url = 'https://fortnite-public-api.theapinetwork.com/prod09/users/id'
        data = {'username': self.username}
        communication = Communication.objects.create(
            player=self,
            method='get_user_id',
            url=url,
        )
        response = communication.communicate(**data)
        self.uid = response['uid']
        self.platforms = response['platforms']
        self.seasons = response['seasons']
        self.save()



class PlayerStats(models.Model):
    player = models.ForeignKey(
        'players.Player', related_name='statuses', on_delete=models.CASCADE,
    )
    data = JSONField(null=True, blank=True)

    date_added = models.DateTimeField(auto_now_add=True)
    date_changed = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Status # {self.id} - {self.player.username}'

    class Meta:
        verbose_name_plural = 'player statuses'
