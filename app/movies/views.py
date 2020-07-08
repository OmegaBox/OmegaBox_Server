from django.db.models import Q, Count, Sum
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Movie
from .serializers import MovieSerializer, MovieDetailSerializer


class MovieListView(ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class MovieDetailView(RetrieveAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieDetailSerializer


class AgeBookingCountView(APIView):
    def get(self, request, pk):
        age_booking_count = Movie.objects.filter(
            pk=pk
        ).values(
            'schedules__reservations__member__id'
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
            ),
        ).aggregate(
            Sum('teens'), Sum('twenties'), Sum('thirties'),
            Sum('fourties'), Sum('fifties')
        )

        return Response({
            '10': age_booking_count['teens__sum'],
            '20': age_booking_count['twenties__sum'],
            '30': age_booking_count['thirties__sum'],
            '40': age_booking_count['fourties__sum'],
            '50': age_booking_count['fifties__sum']
        })
