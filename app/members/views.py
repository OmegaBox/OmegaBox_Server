from django.contrib.auth import get_user_model
from rest_auth.registration.views import RegisterView
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAdminUser

from .permissions import IsAuthorizedMember
from .serializers import SignUpSerializer, MemberDetailSerializer

Member = get_user_model()


class SignUpView(RegisterView):
    serializer_class = SignUpSerializer


class MemberRetrieveView(RetrieveAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberDetailSerializer
    permission_classes = [IsAuthorizedMember, IsAdminUser, ]
