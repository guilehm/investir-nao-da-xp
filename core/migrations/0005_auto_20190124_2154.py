# Generated by Django 2.1.5 on 2019-01-24 23:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_item'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='item_id',
        ),
        migrations.AddField(
            model_name='item',
            name='description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='identifier',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='item',
            name='last_update',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='upcoming',
            field=models.SmallIntegerField(blank=True, null=True),
        ),
    ]