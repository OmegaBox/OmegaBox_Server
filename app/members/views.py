from django.contrib.auth import get_user_model
from rest_auth.registration.views import RegisterView

from .serializers import SignUpSerializer

Member = get_user_model()


class SignUpView(RegisterView):
    serializer_class = SignUpSerializer
