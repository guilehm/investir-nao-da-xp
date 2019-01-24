from django.db import models


class SeasonManager(models.QuerySet):
    def only_available(self):
        return self.filter(statuses__isnull=False).distinct()


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
    number = models.SmallIntegerField(null=True, blank=True)

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
        ordering = ('-name',)
