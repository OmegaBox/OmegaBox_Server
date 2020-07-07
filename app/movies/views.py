from django.db.models import Case, When, Value, Q, CharField, Count, Subquery
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from members.models import Member
from .models import Movie
from .serializers import MovieSerializer, MovieDetailSerializer


class MovieListView(ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class MovieDetailView(RetrieveAPIView):
    serializer_class = MovieDetailSerializer

    def get_queryset(self):
        queryset = Movie.objects.all()

        age_type = queryset.values('name_kor', 'schedules__reservations__member').annotate(
            teens=Count(
                'schedules__reservations__member',
                filter=Q(schedules__reservations__member__birth_date__year__lt=2010) &
                       Q(schedules__reservations__member__birth_date__year__gt=2000),
            ),
            twenties=Count(
                'schedules__reservations__member',
                filter=Q(schedules__reservations__member__birth_date__year__lt=2000) &
                       Q(schedules__reservations__member__birth_date__year__gt=1990),
            )
        )

        return queryset


class AgeBookingCount(APIView):
    def get(self, request, pk):
        movie = Movie.objects.get(pk=pk)
        teens = movie.schedules.filter(
            reservations__member__birth_date__year__gt=2000
        ).filter(
            reservations__member__birth_date__year__lt=2010
        )
        return Response({
            '10': teens.count(),
            # '20': twenties.count(),
            # '30': thirties.count(),
            # '40': fourties.count()
        })
