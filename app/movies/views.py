from django.db.models import Q, Count, Sum
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.permissions import AllowAny

from .models import Movie
from .serializers import MovieSerializer, MovieDetailSerializer, AgeBookingSerializer


class MovieListView(ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class MovieDetailView(RetrieveAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieDetailSerializer


# 수정 필요
class AgeBookingView(ListAPIView):
    serializer_class = AgeBookingSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        queryset = Movie.objects.filter(
            pk=self.kwargs['pk']
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
            Sum('teens'), Sum('twenties'), Sum('thirties'), Sum('fourties'), Sum('fifties')
        )
        return queryset
