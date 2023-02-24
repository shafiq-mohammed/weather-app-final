from django.db import models

#
# class WeatherStation(models.Model):
#     name = models.CharField(max_length=100)
#     state = models.CharField(max_length=2)
#     station_id = models.CharField(max_length=11, unique=True, null=True, blank=True)
#
#     def __str__(self):
#         return self.name


class WeatherData(models.Model):
    station_id = models.CharField(max_length=11, null=True, blank=True)
    date = models.DateField()
    max_temperature = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    min_temperature = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    precipitation = models.DecimalField(max_digits=6, decimal_places=2, null=True)

    def __str__(self):
        return f"{self.station.name} - {self.date}"

    # class Meta:
    #     unique_together = (('date', 'station'),)

    def __str__(self):
        return f'{self.station.name} - {self.date}'


class Statistics(models.Model):
    year = models.IntegerField()
    station = models.ForeignKey(WeatherData, on_delete=models.CASCADE, related_name='statistics')
    avg_max_temperature = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    avg_min_temperature = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    total_precipitation = models.DecimalField(max_digits=8, decimal_places=2, null=True)

    class Meta:
        unique_together = (('year', 'station'),)

    def __str__(self):
        return f'{self.station.name} - {self.year}'

