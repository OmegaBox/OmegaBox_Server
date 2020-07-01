from datetime import datetime

from django.db.models import Count
from rest_framework.generics import ListAPIView

from .models import Schedule, Theater
from .serializers import ScheduleSerializer, ScheduleTheaterListSerializer, ScheduleRegionCountSerializer


class ScheduleList(ListAPIView):
    serializer_class = ScheduleSerializer

    def get_queryset(self):
        date_int = self.kwargs['date']
        theater_id = self.kwargs['theater_id']

        date = datetime.strptime(str(date_int), '%y%m%d')

        queryset = Schedule.objects.filter(
            start_time__date=date,
            screen__theater_id=theater_id,
        )

        # time = self.request.query_params.get('time', None)
        #
        # if time is not None:
        #     time = datetime.strptime(str(time), '%H')
        #     queryset = queryset.filter(start_time__time__gte=time)
        return queryset


class ScheduleTheaterList(ListAPIView):
    serializer_class = ScheduleTheaterListSerializer

    def get_queryset(self):
        date_int = self.kwargs['date']
        date = datetime.strptime(str(date_int), '%y%m%d')
        return Theater.objects.filter(screens__schedules__start_time__date=date).distinct('id')


class ScheduleRegionCount(ListAPIView):
    serializer_class = ScheduleRegionCountSerializer

    def get_queryset(self):
        date_int = self.kwargs['date']
        date = datetime.strptime(str(date_int), '%y%m%d')

        # 중복된 상영관 존재
        return Theater.objects \
            .filter(screens__schedules__start_time__date=date) \
            .values('region', 'region__name') \
            .annotate(region_count=Count('screens'))
