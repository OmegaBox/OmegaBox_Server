from django.urls import path

from .views import (
    SignUpView, MemberDetailView, LoginView, LogoutView, TokenRefreshView, TokenVerifyView,
    CheckUsernameDuplicateView
)

urlpatterns = [
    path('signup/', SignUpView.as_view()),
    path('signup/check-username/', CheckUsernameDuplicateView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('token/verify/', TokenVerifyView.as_view()),

    path('<int:pk>/', MemberDetailView.as_view()),
]
