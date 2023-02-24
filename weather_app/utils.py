import os
from .models import WeatherData, Statistics
from datetime import datetime
from django.db.models import Avg, Sum


def ingest_weather_data():
    weather_data_dir = os.path.join(os.getcwd(), 'wx_data')

    for filename in os.listdir(weather_data_dir):
        if filename.endswith('.txt'):
            filepath = os.path.join(weather_data_dir, filename)
            station_id = filename.split('.')[0]

            with open(filepath, 'r') as f:
                for line in f:
                    parts = line.strip().split('\t')
                    date = parts[0]
                    # date_string = "19850101"
                    date = datetime.strptime(date, "%Y%m%d")
                    max_temp = parts[1]
                    min_temp = parts[2]
                    precipitation = parts[3]

                    # Skip lines with missing values
                    if max_temp == '-9999' or min_temp == '-9999' or precipitation == '-9999':
                        continue

                    # Create or update the WeatherData object
                    defaults = {
                        'max_temperature': max_temp,
                        'min_temperature': min_temp,
                        'precipitation': precipitation
                    }
                    obj, created = WeatherData.objects.update_or_create(
                        station__station_id=station_id, date=date, defaults=defaults
                    )

                    if created:
                        print(f"Created new record for {station_id} on {date}")
                    else:
                        print(f"Updated record for {station_id} on {date}")


def calculate_statistics(station, year):
    # Get weather data for the given station and year
    data = WeatherData.objects.filter(station=station, date__year=year)

    # Calculate average max temperature, average min temperature, and total precipitation
    avg_max_temp = data.aggregate(avg_max_temp=Avg('max_temperature'))['avg_max_temp']
    avg_min_temp = data.aggregate(avg_min_temp=Avg('min_temperature'))['avg_min_temp']
    total_precipitation = data.aggregate(total_precipitation=Sum('precipitation'))['total_precipitation']

    # Create a dictionary containing the calculated statistics
    stats = {
        'year': year,
        'station': station,
        'avg_max_temperature': avg_max_temp,
        'avg_min_temperature': avg_min_temp,
        'total_precipitation': total_precipitation
    }
    """ store the stats in the database """
    Statistics.objects.update_or_create(
        year=year, station=station, defaults=stats
    )

    return stats