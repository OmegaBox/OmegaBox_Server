from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListAPIView, RetrieveAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from reservations.models import Reservation
from utils.custom_functions import calculate_seat_price
from utils.excepts import InvalidScheduleIdException, SeatNamesMissingException
from .models import Schedule, Theater, Screen, SeatType
from .params import (
    movies_query_param, adults_query_param, teens_query_param, preferentials_query_param, seat_names_query_param
)
from .serializers import (
    ScheduleMovieSerializer, ScheduleTheaterListSerializer, ScheduleRegionCountSerializer,
    SeatListSerializer,
    ScreenDetailSerializer, SeatsTotalPriceSerializer, TotalAndReservedSeatsCountSerializer, SeatIDListSerializer
)


@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_summary='Theaters List on Given Date',
    operation_description='해당 날짜에 상영 중인 상영관 리스트',
    manual_parameters=[movies_query_param],
))
class TheatersGivenDateList(ListAPIView):
    serializer_class = ScheduleTheaterListSerializer

    def get_queryset(self):
        date_int = self.kwargs['date']
        date = datetime.strptime(str(date_int), '%y%m%d')

        movies = self.request.query_params.get('movies', None)

        if movies is not None:
            movies_list = list(map(int, movies.split()))[:3]
            queryset = Theater.objects.filter(
                screens__schedules__movie__in=movies_list,
                screens__schedules__start_time__date=date,
            ).distinct('id')
        else:
            queryset = Theater.objects.filter(screens__schedules__start_time__date=date).distinct('id')

        return queryset.select_related('region')


@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_summary='Theaters Region Count on Given Date',
    operation_description='해당 날짜에 상영 중인 상영관들 지역 기준 합산',
    manual_parameters=[movies_query_param],
))
class TheatersRegionCountGivenDate(ListAPIView):
    serializer_class = ScheduleRegionCountSerializer

    def get_queryset(self):
        date_int = self.kwargs['date']
        date = datetime.strptime(str(date_int), '%y%m%d')

        movies = self.request.query_params.get('movies', None)

        if movies is not None:
            movies_list = list(map(int, movies.split()))[:3]
            queryset = Theater.objects.filter(
                screens__schedules__movie__in=movies_list,
                screens__schedules__start_time__date=date,
            ).values(
                'region', 'region__name'
            ).annotate(Count('name', distinct=True))

        else:
            queryset = Theater.objects.filter(
                screens__schedules__start_time__date=date,
            ).values(
                'region', 'region__name'
            ).annotate(
                Count('name', distinct=True)
            )

        return queryset


@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_summary='Seats Total Price Before Payment',
    operation_description='결제 전 최종결제금액 출력',
    manual_parameters=[adults_query_param, teens_query_param, preferentials_query_param],
    responses={200: SeatsTotalPriceSerializer()}
))
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


@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_summary='Reserved Seat List of a Schedule',
    operation_description='해당 스케쥴의 예약된 좌석 정보',
))
class ReservedSeatList(ListAPIView):
    serializer_class = SeatListSerializer
    pagination_class = None

    def get_queryset(self):
        schedule_id = int(self.kwargs['schedule_id'])
        try:
            schedule = Schedule.objects.get(pk=schedule_id)
            return Reservation.objects.filter(schedule=schedule).values('seat_grades__seat__name')
        except ObjectDoesNotExist:
            raise InvalidScheduleIdException


@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_summary='Total Seats Count & Reserved Seats Count of a Schedule',
    operation_description='해당 스케쥴의 전체좌석 및 예약 좌석 합계',
    responses={200: TotalAndReservedSeatsCountSerializer()}
))
class TotalAndReservedSeatsCount(APIView):
    def get(self, request, schedule_id):
        try:
            schedule = Schedule.objects.get(pk=schedule_id)
            return Response({
                'total_seats': schedule.seat_types.filter(type='general').count(),
                'reserved_seats': schedule.seat_types.aggregate(
                    reserved_seats=Count('seat__reservations'))['reserved_seats']
            })
        except ObjectDoesNotExist:
            raise InvalidScheduleIdException


@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_summary='Screen Detail',
    operation_description='해당 스크린의 상세 정보',
))
class ScreenDetail(RetrieveAPIView):
    queryset = Screen.objects.all()
    serializer_class = ScreenDetailSerializer
    lookup_url_kwarg = 'screen_id'


@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_summary='Seat ID List',
    operation_description='스케쥴 ID와 좌석 이름을 입력받아 각 좌석 ID를 반환',
    responses={200: SeatIDListSerializer(many=True)},
    manual_parameters=[seat_names_query_param]
))
class SeatIDList(APIView):
    def get(self, request, schedule_id):
        schedule = get_object_or_404(Schedule, pk=schedule_id)
        seat_names = self.request.query_params.get('names', None)

        if seat_names is not None:
            seats_list = list(seat_names.split())

            seat_type_qs = SeatType.objects.filter(
                schedule=schedule,
                seat__name__in=seats_list
            ).prefetch_related('seat')
            return Response(SeatIDListSerializer(seat_type_qs, many=True).data)
        else:
            raise SeatNamesMissingException


@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_summary='Schedules List on Given Date',
    operation_description='해당 상영관 특정 날짜의 스케쥴 정보',
    manual_parameters=[movies_query_param],
))
class ScheduleListGivenDate(ListAPIView):
    serializer_class = ScheduleMovieSerializer

    def get_queryset(self):
        date_int = self.kwargs.get('date', None)
        date = datetime.strptime(str(date_int), '%y%m%d')

        theater_id = self.kwargs.get('theater_id', None)

        movies = self.request.query_params.get('movies', None)

        if movies is not None:
            movies_list = list(map(int, movies.split()))[:3]
            queryset = Schedule.objects.filter(
                movie__in=movies_list,
                start_time__date=date,
                screen__theater_id=theater_id,
            )
        else:
            queryset = Schedule.objects.filter(
                start_time__date=date,
                screen__theater_id=theater_id,
            )
        return queryset.select_related('movie', 'screen__theater__region').prefetch_related('seat_types')
