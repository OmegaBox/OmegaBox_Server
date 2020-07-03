from rest_framework.generics import ListCreateAPIView

from .models import Movie
from .serializers import MovieSerializer


class MovieList(ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
