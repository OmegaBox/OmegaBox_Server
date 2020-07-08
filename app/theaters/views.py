from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from rest_framework.generics import ListAPIView, RetrieveAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from utils import calculate_seat_price
from utils.excepts import InvalidScheduleIDException
from .models import Schedule, Theater, Screen
from .serializers import (
    ScheduleMovieSerializer, ScheduleTheaterListSerializer, ScheduleRegionCountSerializer,
    SeatListSerializer,
    ScreenDetailSerializer)


# 해당 상영관의 상영시간 정보
class ScheduleList(ListAPIView):
    serializer_class = ScheduleMovieSerializer

    def get_queryset(self):
        date_int = self.kwargs.get('date', None)
        date = datetime.strptime(str(date_int), '%y%m%d')

        theater_id = self.kwargs.get('theater_id', None)

        movies = self.request.query_params.get('movies', None)

        if movies is not None:
            movies_list = list(movies)[:3]
            queryset = Schedule.objects.filter(
                movie__in=movies_list
            ).filter(
                start_time__date=date,
                screen__theater_id=theater_id,
            )
        else:
            queryset = Schedule.objects.filter(
                start_time__date=date,
                screen__theater_id=theater_id,
            )

        return queryset


# 상영 중인 상영관 정보
class ScheduleTheaterList(ListAPIView):
    serializer_class = ScheduleTheaterListSerializer

    def get_queryset(self):
        date_int = self.kwargs['date']

        date = datetime.strptime(str(date_int), '%y%m%d')

        movies = self.request.query_params.get('movies', None)

        if movies is not None:
            movies_list = list(movies)[:3]
            queryset = Theater.objects.filter(
                screens__schedules__movie__in=movies_list
            ).filter(
                screens__schedules__start_time__date=date
            ).distinct('id')
        else:
            queryset = Theater.objects.filter(screens__schedules__start_time__date=date).distinct('id')

        return queryset


# 상영 중인 상영관 지역 기준 합산
class ScheduleRegionCount(ListAPIView):
    serializer_class = ScheduleRegionCountSerializer

    def get_queryset(self):
        date_int = self.kwargs['date']

        date = datetime.strptime(str(date_int), '%y%m%d')
        movies = self.request.query_params.get('movies', None)

        if movies is not None:
            movies_list = list(movies)[:3]
            queryset = Theater.objects.filter(
                screens__schedules__movie__in=movies_list
            ).filter(
                screens__schedules__start_time__date=date
            ).values(
                'region', 'region__name'
            ).annotate(Count('name', distinct=True))

        else:
            queryset = Theater.objects.filter(
                screens__schedules__start_time__date=date
            ).values(
                'region', 'region__name'
            ).annotate(
                Count('name', distinct=True)
            )

        return queryset


# 해당 스케쥴의 예약된 좌석 정보
class SeatList(ListAPIView):
    serializer_class = SeatListSerializer
    pagination_class = None

    def get_queryset(self):
        schedule_id = int(self.kwargs['schedule_id'])
        try:
            schedule = Schedule.objects.get(pk=schedule_id)
            return schedule.seat_types.exclude(
                type='sit_apart',
            ).exclude(
                seat__reservations__isnull=True,
            )
        except ObjectDoesNotExist:
            raise InvalidScheduleIDException


# 해당 스케쥴의 전체좌석 및 예약 좌석 합계
class SeatCount(APIView):
    def get(self, request, schedule_id):
        try:
            schedule = Schedule.objects.get(pk=schedule_id)
            return Response({
                'total_seats': schedule.seat_types.count(),
                'reserved_seats': schedule.seat_types.aggregate(
                    reserved_seats=Count('seat__reservations'))['reserved_seats']
            })
        except ObjectDoesNotExist:
            raise InvalidScheduleIDException


class ScreenDetail(RetrieveAPIView):
    queryset = Screen.objects.all()
    serializer_class = ScreenDetailSerializer
    lookup_url_kwarg = 'screen_id'


# 결제 전 최종결제금액 출력
class SeatsTotalPrice(APIView):
    def get(self, request, schedule_id):
        schedule = get_object_or_404(Schedule, pk=schedule_id)
        screen_type = schedule.screen.screen_type

        adults = request.query_params.get('adults', None)
        teens = request.query_params.get('teens', None)
        preferentials = request.query_params.get('preferentials', None)

        total_price = 0

        if adults is not None:
            total_price += calculate_seat_price(screen_type, 'adult') * int(adults)

        if teens is not None:
            total_price += calculate_seat_price(screen_type, 'teen') * int(teens)

        if preferentials is not None:
            total_price += calculate_seat_price(screen_type, 'preferential') * int(preferentials)

        return Response({
            "total_price": total_price,
        })
