import uuid

import requests
from django.contrib.postgres.fields import JSONField
from django.db import models

from xp.settings import FORTNITE_AUTH_KEY

HEADERS = {'Authorization': FORTNITE_AUTH_KEY}


class Communication(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    player = models.ForeignKey(
        'players.Player',
        related_name='communications',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    method = models.CharField(max_length=100)
    url = models.URLField(max_length=200)
    data = JSONField(null=True, blank=True)

    date_added = models.DateTimeField(auto_now_add=True)
    date_changed = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Communication #{self.id}'

    def communicate(self, **data):
        response = requests.post(
            url=self.url, headers=HEADERS, data=dict(data)
        )
        self.data = response.json()
        self.save()
        if response.status_code == 200:
            return self.data
