from django.contrib.postgres.fields import JSONField
from django.db import models

from communications.models import Communication
from core.models import Platform, Season


class Player(models.Model):
    uid = models.CharField(max_length=100, unique=True, db_index=True, null=True, blank=True)
    username = models.CharField(max_length=50, unique=True)
    platforms = models.ManyToManyField('core.Platform', related_name='players', blank=True)
    seasons = models.ManyToManyField('core.Season', related_name='players', blank=True)

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
        self.uid = response.get('uid')
        self.save()

        platforms_data = response.get('platforms')
        platforms = [Platform.objects.get_or_create(name=name) for name in platforms_data]
        self.platforms.add(*[platform[0] for platform in platforms])

        seasons_data = response.get('seasons')
        seasons = [Season.objects.get_or_create(name=name) for name in seasons_data]
        self.seasons.add(*[season[0] for season in seasons])

        return response

    def get_stats(self, platform_name='pc'):
        if not self.uid:
            return self.get_user_data()
        url = 'https://fortnite-public-api.theapinetwork.com/prod09/users/public/br_stats'
        data = {
            'user_id': self.uid,
            'platform': self.platforms.get(name=platform_name).name,
            'window': 'alltime',
        }
        communication = Communication.objects.create(
            player=self,
            method='get_stats',
            url=url,
        )
        response = communication.communicate(**data)
        stats = PlayerStats.objects.create(
            player=self,
            data=response,
        )
        return stats.data


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
