# Generated by Django 4.1.7 on 2023-02-23 17:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('weather_app', '0002_weatherstation_station_id'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='weatherdata',
            unique_together=set(),
        ),
    ]
