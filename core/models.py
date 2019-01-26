from django.contrib.postgres.fields import JSONField
from django.db import models


class SeasonManager(models.QuerySet):
    def only_available(self):
        return self.filter(statuses__isnull=False).distinct()

    def last_season(self):
        return self.only_available().last()


class Platform(models.Model):
    epic_id = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=100, unique=True)
    name_long = models.CharField(max_length=100, null=True, blank=True)

    date_added = models.DateTimeField(auto_now_add=True)
    date_changed = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name_long}'


class Season(models.Model):
    name = models.CharField(max_length=100, unique=True)
    number = models.SmallIntegerField(null=True, blank=True, db_index=True)

    date_added = models.DateTimeField(auto_now_add=True)
    date_changed = models.DateTimeField(auto_now=True)

    objects = SeasonManager.as_manager()

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        if not self.number:
            self.number = ''.join([char for char in self.name if char.isdigit()]) or 0
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('number',)


class Item(models.Model):
    identifier = models.CharField(max_length=100, unique=True, null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    upcoming = models.SmallIntegerField(null=True, blank=True)
    cost = models.DecimalField(decimal_places=0, max_digits=9, null=True, blank=True)
    captial = models.CharField(max_length=50, null=True, blank=True)
    type = models.CharField(max_length=50, null=True, blank=True)
    rarity = models.CharField(max_length=50, null=True, blank=True)
    obtained = models.CharField(max_length=50, null=True, blank=True)
    obtained_type = models.CharField(max_length=50, null=True, blank=True)
    featured = models.SmallIntegerField(null=True, blank=True)
    refundable = models.SmallIntegerField(null=True, blank=True)
    ratings = JSONField(null=True, blank=True)
    last_update = models.CharField(max_length=50, null=True, blank=True)
    is_upcoming = models.BooleanField(default=False)

    youtube = models.URLField(null=True, blank=True)
    image = models.URLField(null=True, blank=True)
    image_transparent = models.URLField(null=True, blank=True)
    image_background = models.URLField(null=True, blank=True)
    image_information = models.URLField(null=True, blank=True)
    image_featured_transparent = models.URLField(null=True, blank=True)

    data = JSONField(null=True, blank=True)

    date_added = models.DateTimeField(auto_now_add=True, db_index=True)
    date_changed = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Items #{self.id}'

    class Meta:
        ordering = ('-id',)
