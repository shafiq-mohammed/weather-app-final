# Generated by Django 4.1.7 on 2023-02-23 17:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('weather_app', '0003_alter_weatherdata_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weatherdata',
            name='station',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='weather_app.weatherstation'),
        ),
    ]
