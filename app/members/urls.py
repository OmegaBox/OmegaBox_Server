from django.urls import path

from .views import (
    SignUpView, MemberRetrieveView, LoginView, LogoutView, TokenRefreshView, TokenVerifyView
)

urlpatterns = [
    path('signup/', SignUpView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('token/verify/', TokenVerifyView.as_view()),

    path('<int:pk>/', MemberRetrieveView.as_view()),
]
