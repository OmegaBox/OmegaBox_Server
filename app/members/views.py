from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_auth.registration.views import RegisterView
from rest_auth.views import (
    LogoutView as DefaultLogoutView, LoginView as DefaultLoginView
)
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework_simplejwt.views import (
    TokenRefreshView as DefaultTokenRefreshView,
    TokenVerifyView as DefaultTokenVerifyView,
)

from .permissions import IsAuthorizedMember
from .serializers import SignUpSerializer, MemberDetailSerializer, LoginSerializer, TokenRefreshSerializer, \
    TokenRefreshResultSerializer

Member = get_user_model()


@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_summary='Sign Up',
    operation_description='회원가입',
))
class SignUpView(RegisterView):
    serializer_class = SignUpSerializer


@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_summary='Log In',
    operation_description='로그인',
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
class MemberRetrieveView(RetrieveAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberDetailSerializer
    permission_classes = [IsAuthorizedMember, IsAdminUser, ]
