from django.urls import path
from rest_auth.views import LogoutView, LoginView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)

from .views import SignUpView, MemberRetrieveView, MemberListView

urlpatterns = [
    path('signup/', SignUpView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('token/verify/', TokenVerifyView.as_view()),

    path('', MemberListView.as_view()),
    path('<int:id>/', MemberRetrieveView.as_view()),
]
