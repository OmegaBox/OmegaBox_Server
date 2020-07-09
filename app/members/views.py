from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from rest_auth.registration.views import RegisterView
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from utils.excepts import UsernameDuplicateException
from .permissions import IsAuthorizedMember
from .serializers import SignUpSerializer, MemberDetailSerializer

Member = get_user_model()


class SignUpView(RegisterView):
    serializer_class = SignUpSerializer


class MemberRetrieveView(RetrieveAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberDetailSerializer
    permission_classes = [IsAuthorizedMember, IsAdminUser, ]


class UsernameDuplicateView(APIView):
    def post(self, request):
        username = request.data['username']
        try:
            Member.objects.get(username=username)
            raise UsernameDuplicateException
        except ObjectDoesNotExist:
            return Response({"detail": '사용가능한 아이디입니다.'}, status=status.HTTP_200_OK)
