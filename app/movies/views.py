from django.db.models import Q, Count, Sum
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import RetrieveAPIView, ListAPIView

from .models import Movie
from .serializers import MovieSerializer, MovieDetailSerializer, AgeBookingSerializer


@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_summary='Movie List',
    operation_description='전체 영화 정보',
))
class MovieListView(ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_summary='Movie Detail',
    operation_description='영화 상세 정보',
))
class MovieDetailView(RetrieveAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieDetailSerializer


@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_summary='Age Booking',
    operation_description='해당 영화의 나이대별 예매 총합',
))
class AgeBookingView(RetrieveAPIView):
    serializer_class = AgeBookingSerializer

    def get_object(self):
        aggregated_dict = Movie.objects.filter(
            pk=self.kwargs['pk']
        ).values(
            'schedules__reservations__member'
        ).annotate(
            teens=Count(
                'schedules__reservations__member',
                filter=Q(schedules__reservations__member__birth_date__year__lt=2010) &
                       Q(schedules__reservations__member__birth_date__year__gt=2000),
            ),
            twenties=Count(
                'schedules__reservations__member',
                filter=Q(schedules__reservations__member__birth_date__year__lt=2000) &
                       Q(schedules__reservations__member__birth_date__year__gt=1990),
            ),
            thirties=Count(
                'schedules__reservations__member',
                filter=Q(schedules__reservations__member__birth_date__year__lt=1990) &
                       Q(schedules__reservations__member__birth_date__year__gt=1980),
            ),
            fourties=Count(
                'schedules__reservations__member',
                filter=Q(schedules__reservations__member__birth_date__year__lt=1980) &
                       Q(schedules__reservations__member__birth_date__year__gt=1970),
            ),
            fifties=Count(
                'schedules__reservations__member',
                filter=Q(schedules__reservations__member__birth_date__year__lt=1970) &
                       Q(schedules__reservations__member__birth_date__year__gt=1960),
            )
        ).aggregate(
            Sum('teens'), Sum('twenties'), Sum('thirties'),
            Sum('fourties'), Sum('fifties')
        )

        return aggregated_dict
