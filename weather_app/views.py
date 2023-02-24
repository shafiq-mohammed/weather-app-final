
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from weather_app.serializers import *
from weather_app.models import WeatherData, Statistics
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
import os
from datetime import datetime
from weather_app.utils import calculate_statistics


class WeatherDataList(ModelViewSet):
    queryset = WeatherData.objects.all()
    serializer_class = WeatherDataSerializer
    pagination_class = PageNumberPagination
    pagination_class.page_size = 15

    def get_queryset(self):
        queryset = WeatherData.objects.all()

        # Filter by station ID
        station_id = self.request.query_params.get('station_id', None)
        if station_id is not None:
            queryset = queryset.filter(station_id=station_id)

        # Filter by date range
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        if start_date is not None:
            queryset = queryset.filter(date__gte=start_date)
        if end_date is not None:
            queryset = queryset.filter(date__lte=end_date)

        return queryset


class StatisticsViewSet(ModelViewSet):
    queryset = Statistics.objects.all()
    serializer_class = StatisticsSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filter by station ID
        station_id = self.request.query_params.get('station_id', None)
        if station_id is not None:
            queryset = queryset.filter(station_id=station_id)

        # Filter by year
        year = self.request.query_params.get('year', None)
        if year is not None:
            queryset = queryset.filter(year=year)

        return queryset


class StatisticsList(APIView):
    def get(self, request):

        station_id = self.request.query_params.get('station', None)
        year = self.request.query_params.get('year', None)
        if station_id is not None and year is not None:
            station_data = calculate_statistics(station_id, year)
            return Response(station_data)
        else:
            resp = Statistics.objects.all()
            return Response(resp)


class Test_data_upload(APIView):
    def get(self, request):
        weather_data_dir = os.path.join(os.getcwd(), 'wx_data')
        weather_data_list = []
        for filename in os.listdir(weather_data_dir):
            print("DEBUG: Going through file: ", filename)
            if filename.endswith('.txt'):
                filepath = os.path.join(weather_data_dir, filename)
                station_id = filename.split('.')[0]

                # Create the WeatherStation object if it doesn't exist
                # station, created = WeatherStation.objects.get_or_create(station_id=station_id,
                #                                                         defaults={'name': station_id})

                with open(filepath, 'r') as f:
                    for line in f:
                        parts = line.strip().split('\t')
                        date = parts[0]
                        date = datetime.strptime(date, "%Y%m%d")
                        max_temp = parts[1]
                        min_temp = parts[2]
                        precipitation = parts[3]

                        if max_temp == '-9999' or min_temp == '-9999' or precipitation == '-9999':
                            continue

                        # Create the WeatherData object
                        weather_data = WeatherData(
                            date=date,
                            max_temperature=max_temp,
                            min_temperature=min_temp,
                            precipitation=precipitation,
                            station_id=station_id  # use the created WeatherStation instance
                        )
                        weather_data_list.append(weather_data)

        # Bulk create the WeatherData objects
        WeatherData.objects.bulk_create(weather_data_list)

        return Response("Data uploaded")

