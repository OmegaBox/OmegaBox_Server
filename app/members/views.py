import datetime

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_auth.registration.views import RegisterView
from rest_auth.views import (
    LogoutView as DefaultLogoutView, LoginView as DefaultLoginView
)
from rest_framework import status
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import (
    TokenRefreshView as DefaultTokenRefreshView,
    TokenVerifyView as DefaultTokenVerifyView,
)

from movies.models import Movie, Rating
from movies.serializers import LikeMoviesSerializer, WatchedMoviesSerializer, RatingMoviesSerializer
from reservations.models import Reservation
from utils.excepts import UsernameDuplicateException
from .permissions import IsAuthorizedMember
from .serializers import SignUpSerializer, MemberDetailSerializer, LoginSerializer, TokenRefreshSerializer, \
    TokenRefreshResultSerializer, JWTSerializer, CheckUsernameDuplicateSerializer, ReservedMoviesSerializer, \
    CanceledReservationMoviesSerializer

Member = get_user_model()


@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_summary='Sign Up',
    operation_description='회원가입',
    responses={200: JWTSerializer()},
))
class SignUpView(RegisterView):
    serializer_class = SignUpSerializer


@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_summary='Check Username Duplicate',
    operation_description='아이디 중복 확인',
    request_body=CheckUsernameDuplicateSerializer(),
    responses={200: ''},
))
class CheckUsernameDuplicateView(APIView):
    def post(self, request):
        username = request.data['username']
        try:
            Member.objects.get(username=username)
            raise UsernameDuplicateException
        except ObjectDoesNotExist:
            return Response({}, status=status.HTTP_200_OK)


@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_summary='Log In',
    operation_description='로그인',
    responses={200: JWTSerializer()},
))
class LoginView(DefaultLoginView):
    serializer_class = LoginSerializer


@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_summary='Log Out',
    operation_description='로그아웃',
))
class LogoutView(DefaultLogoutView):
    def _allowed_methods(self):
        return ['GET']


@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_summary='Token Refresh',
    operation_description='Refresh Token을 통해 만료된 Access Token 재발급',
    responses={200: TokenRefreshResultSerializer()}
))
class TokenRefreshView(DefaultTokenRefreshView):
    serializer_class = TokenRefreshSerializer


@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_summary='Access Token Verify',
    operation_description='Access Token이 유효한지 확인',
    responses={200: ''}
))
class TokenVerifyView(DefaultTokenVerifyView):
    pass


@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_summary='Member Detail',
    operation_description='회원 상세 정보',
))
class MemberDetailView(RetrieveAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberDetailSerializer
    permission_classes = [IsAuthorizedMember, IsAdminUser, ]


class LikeMoviesView(ListAPIView):
    serializer_class = LikeMoviesSerializer
    permission_classes = [IsAuthenticated, IsAdminUser, ]

    def get_queryset(self):
        return Movie.objects.filter(like_members__pk=self.kwargs['pk'], movie_likes__liked=True).order_by('movie_likes')


class RatingMoviesView(ListAPIView):
    serializer_class = RatingMoviesSerializer
    permission_classes = [IsAuthenticated, IsAdminUser, ]

    def get_queryset(self):
        return Rating.objects.filter(member__pk=self.kwargs['pk']).order_by('created_at')


# Movie가 아닌 Payment별 분리로 변경 검토
class WatchedMoviesView(ListAPIView):
    serializer_class = WatchedMoviesSerializer
    permission_classes = [IsAuthenticated, IsAdminUser, ]

    def get_queryset(self):
        return Movie.objects.filter(
            schedules__reservations__member__pk=self.kwargs['pk'],
            schedules__reservations__payment__isnull=False,
            schedules__start_time__lte=datetime.datetime.today()
        ).distinct().order_by('schedules__start_time')


class ReservedMoviesView(ListAPIView):
    serializer_class = ReservedMoviesSerializer

    def get_queryset(self):
        return Reservation.objects.filter(
            schedule__start_time__gt=datetime.datetime.today(),
            member__pk=self.kwargs['pk'],
            payment__isnull=False
        ).distinct().order_by('reserved_at')


class CanceledReservationMoviesView(ListAPIView):
    serializer_class = CanceledReservationMoviesSerializer

    def get_queryset(self):
        return Reservation.objects.filter(
            schedule__start_time__lte=datetime.datetime.today(),
            member__pk=self.kwargs['pk'],
            payment__is_canceled=True
        ).order_by('payment.canceled_at')
