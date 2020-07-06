from django.contrib.auth import get_user_model
from rest_auth.registration.views import RegisterView
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Profile
from .serializers import SignUpSerializer, ProfileDetailSerializer, MemberSerializer

Member = get_user_model()


class SignUpView(RegisterView):
    serializer_class = SignUpSerializer


class ProfileDetailView(RetrieveAPIView):
    serializer_class = ProfileDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Profile.objects.get_or_create(member=self.request.user)[0]


class MemberListView(ListAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
