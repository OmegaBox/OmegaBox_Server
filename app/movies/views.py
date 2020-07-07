from django.db.models import Case, When, Value, Q, CharField, Count, Subquery
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Movie
from .serializers import MovieSerializer, MovieDetailSerializer


class MovieListView(ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAdminUser, IsAuthenticatedOrReadOnly, ]


class MovieDetailView(RetrieveAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieDetailSerializer
    permission_classes = [IsAdminUser, IsAuthenticatedOrReadOnly, ]


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
