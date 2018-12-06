from django.db import models


class Player(models.Model):
    uid = models.CharField(max_length=100)
    username = models.CharField(max_length=50)
    platforms = models.CharField(max_length=100)

    date_added = models.DateTimeField(auto_now_add=True)
    date_changed = models.DateTimeField(auto_now=True)
