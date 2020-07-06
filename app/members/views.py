from django.contrib.auth import get_user_model
from rest_auth.registration.views import RegisterView
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAdminUser

from .permissions import IsAuthorizedMember
from .serializers import SignUpSerializer, MemberSerializer

Member = get_user_model()


class SignUpView(RegisterView):
    serializer_class = SignUpSerializer


class MemberListView(ListAPIView):
    serializer_class = MemberSerializer
    permission_classes = [IsAdminUser, ]

    def get_queryset(self):
        return Member.objects.all()


class MemberRetrieveView(RetrieveAPIView):
    lookup_field = 'id'
    serializer_class = MemberSerializer
    permission_classes = [IsAuthorizedMember, IsAdminUser, ]

    def get_queryset(self):
        return Member.objects.all()
