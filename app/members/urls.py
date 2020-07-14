from django.urls import path

from .views import (
    SignUpView, MemberDetailView, LoginView, LogoutView, TokenRefreshView, TokenVerifyView,
    CheckUsernameDuplicateView, LikeMoviesView, WatchedMoviesView, RatingMoviesView, ReservedMoviesView,
    CanceledReservationMoviesView
)

urlpatterns = [
    path('signup/', SignUpView.as_view()),
    path('signup/check-username/', CheckUsernameDuplicateView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('token/verify/', TokenVerifyView.as_view()),

    path('detail/', MemberDetailView.as_view()),
    path('like-movies/', LikeMoviesView.as_view()),
    path('watched-movies/', WatchedMoviesView.as_view()),
    path('rating-movies/', RatingMoviesView.as_view()),
    path('reserved-movies/', ReservedMoviesView.as_view()),
    path('reserved-movies/canceled/', CanceledReservationMoviesView.as_view()),

]
