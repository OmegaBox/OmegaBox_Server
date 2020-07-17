from django.db.models import Q, Count, Sum
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Movie, Rating, MovieLike
from .serializers import (
    MovieSerializer, MovieDetailSerializer, AgeBookingSerializer, RatingsSerializer, MovieLikeSerializer
)


@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_summary='Movie List',
    operation_description='전체 영화 정보',
))
class MovieListView(ListAPIView):
    serializer_class = MovieSerializer

    def get_queryset(self):
        search_name = self.request.query_params.get('searchName', None)
        try:
            if search_name is None:
                queryset = Movie.objects.all()
            else:
                queryset = Movie.objects.filter(
                    Q(name_kor__contains=search_name) |
                    Q(name_eng__icontains=search_name)
                )
        except ValueError as e:
            queryset = Movie.objects.all()
        return queryset


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
        # timedelta를 이용한 계산 변경 검토
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

        # 임의로 데이터 수 올림
        aggregated_dict['teens__sum'] = (aggregated_dict['teens__sum'] + 3) * 9
        aggregated_dict['twenties__sum'] = (aggregated_dict['twenties__sum'] + 1) * 7
        aggregated_dict['thirties__sum'] = (aggregated_dict['thirties__sum'] + 5) * 4
        aggregated_dict['fourties__sum'] = (aggregated_dict['fourties__sum'] + 2) * 9
        aggregated_dict['fifties__sum'] = (aggregated_dict['fifties__sum'] + 3) * 5

        return aggregated_dict


@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_summary='Movie Rating Create',
    operation_description='해당 영화의 한줄평 쓰기(생성)',
))
class RatingCreateView(CreateAPIView):
    serializer_class = RatingsSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return Rating.objects.filter(
            member=self.request.user,
            movie=self.kwargs['pk']
        )

    def perform_create(self, serializer):
        movie = Movie.objects.get(pk=self.kwargs['pk'])
        serializer.save(member=self.request.user, movie=movie)


@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_summary='Movie Like Click',
    operation_description='해당 영화 좋아요 누르기',
))
class MovieLikeCheckView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get_object(self, pk):
        try:
            movie = Movie.objects.get(pk=pk)
            return MovieLike.objects.get(movie=movie, member=self.request.user)
        except MovieLike.DoesNotExist:
            return MovieLike.objects.create(movie=movie, member=self.request.user, liked=False)

    def get(self, request, pk):
        movie_like = self.get_object(pk)
        movie_like.liked = not movie_like.liked
        movie_like.save()
        serializer = MovieLikeSerializer(movie_like)
        return Response(serializer.data)
