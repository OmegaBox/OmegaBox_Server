from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_auth.registration.views import RegisterView
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAdminUser

from .permissions import IsAuthorizedMember
from .serializers import SignUpSerializer, MemberDetailSerializer

Member = get_user_model()


@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_summary='Sign Up',
    operation_description='회원가입',
))
class SignUpView(RegisterView):
    serializer_class = SignUpSerializer


@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_summary='Member Detail',
    operation_description='회원 상세 정보',
))
class MemberRetrieveView(RetrieveAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberDetailSerializer
    permission_classes = [IsAuthorizedMember, IsAdminUser, ]
