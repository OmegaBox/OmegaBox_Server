from rest_framework.generics import ListCreateAPIView

from .models import Movie
from .serializers import MovieSerializer


class MovieList(ListCreateAPIView):
    serializer_class = MovieSerializer

    def get_queryset(self):
        pass

    # def get_age_bookings_count(self, movie):
    #     movie_name = movie.name_kor
    #     members_ages = list()
    #     for schedule in Schedule.objects.filter(movie__name_kor=movie_name):
    #         for reservation in schedule.reservations.all():
    #             members_ages.append(reservation.member.age())
    #     return members_ages
