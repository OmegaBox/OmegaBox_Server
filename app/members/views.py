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
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import (
    TokenRefreshView as DefaultTokenRefreshView,
    TokenVerifyView as DefaultTokenVerifyView,
)

from movies.models import Movie, Rating, MovieLike
from reservations.models import Reservation
from utils.excepts import UsernameDuplicateException
from .serializers import SignUpSerializer, MemberDetailSerializer, LoginSerializer, TokenRefreshSerializer, \
    TokenRefreshResultSerializer, JWTSerializer, CheckUsernameDuplicateSerializer, LikeMoviesSerializer, \
    WatchedMoviesSerializer, RatingMoviesSerializer, ReservedMoviesSerializer, CanceledReservationMoviesSerializer, \
    SocialSignUpSerializer, SocialLoginSerializer

Member = get_user_model()


@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_summary='Sign Up',
    operation_description='회원가입',
    responses={200: JWTSerializer()},
))
class SignUpView(RegisterView):
    serializer_class = SignUpSerializer


@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_summary='Social Sign Up',
    operation_description='소셜 회원가입 - 비밀번호 자동설정(username과 동일)',
    responses={200: JWTSerializer()},
))
class SocialSignUpView(RegisterView):
    serializer_class = SocialSignUpSerializer


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


@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_summary='Social Log In',
    operation_description='소셜 로그인 - username/password: googleId & unique_id: tokenId',
    responses={200: JWTSerializer()},
))
class SocialLoginView(DefaultLoginView):
    serializer_class = SocialLoginSerializer


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
    serializer_class = MemberDetailSerializer
    permission_classes = [IsAuthenticated, ]

    def get_object(self):
        return Member.objects.get(pk=self.request.user.pk)


@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_summary='Timeline Like Movie List per Member',
    operation_description='멤버별 좋아요 누른 영화 리스트 정보'
))
class LikeMoviesView(ListAPIView):
    serializer_class = LikeMoviesSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return MovieLike.objects.select_related(
            'movie', 'member'
        ).filter(
            member=self.request.user,
            liked=True
        )


@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_summary='Watched Movie List per Member',
    operation_description='멤버별 본영화 구매내역 및 상세정보 리스트'
))
class WatchedMoviesView(ListAPIView):
    serializer_class = WatchedMoviesSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return Reservation.objects.select_related(
            'payment', 'schedule__screen__theater__region', 'schedule__movie'
        ).filter(
            schedule__start_time__lte=datetime.datetime.today(),
            member=self.request.user,
            payment__isnull=False,
            payment__is_canceled=False
        ).order_by('schedule__start_time')


@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_summary='Rating Movie List per Member',
    operation_description='멤버별 한줄평쓴 영화 리스트 정보'
))
class RatingMoviesView(ListAPIView):
    serializer_class = RatingMoviesSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return Rating.objects.select_related(
            'movie'
        ).filter(
            member=self.request.user
        ).order_by('created_at')


@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_summary='Reserved Movie List per Member',
    operation_description='멤버별 영화 예매내역 리스트 정보'
))
class ReservedMoviesView(ListAPIView):
    serializer_class = ReservedMoviesSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return Reservation.objects.select_related(
            'member__profile', 'schedule__movie', 'schedule__screen__theater', 'payment'
        ).filter(
            member=self.request.user,
            payment__isnull=False,
            payment__is_canceled=False
        ).order_by('reserved_at')


@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_summary='Canceled Reserved Movie List per Member',
    operation_description='멤버별 영화 예매취소내역 리스트 정보'
))
class CanceledReservationMoviesView(ListAPIView):
    serializer_class = CanceledReservationMoviesSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return Reservation.objects.select_related(
            'member', 'payment', 'schedule__movie', 'schedule__screen__theater'
        ).filter(
            member=self.request.user,
            payment__isnull=False,
            payment__is_canceled=True
        ).order_by('-payment__canceled_at')
