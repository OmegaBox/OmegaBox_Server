from rest_framework.generics import ListCreateAPIView
from .models import Movie
from .serializers import MovieSerializer


class MovieList(ListCreateAPIView):
    lookup_field = 'name_kor'
    serializer_class = MovieSerializer

    def get_queryset(self):
        queryset = Movie.objects.all()
        return queryset
