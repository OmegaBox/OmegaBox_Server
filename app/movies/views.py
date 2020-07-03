from rest_framework import generics
from rest_framework.generics import ListCreateAPIView

from .models import Movie, Rating
from .serializers import MovieSerializer, AgeBookingSerializer


class MovieList(ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class AgeBookingList(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = AgeBookingSerializer
