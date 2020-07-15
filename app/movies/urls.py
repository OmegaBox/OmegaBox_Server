from django.urls import path

from .views import MovieListView, MovieDetailView, AgeBookingView, RatingCreateView, MovieLikeCheckView

urlpatterns = [
    path('', MovieListView.as_view()),
    path('detail/<int:pk>/', MovieDetailView.as_view()),
    path('detail/<int:pk>/age-booking/', AgeBookingView.as_view()),
    path('detail/<int:pk>/rating/create/', RatingCreateView.as_view()),
    path('detail/<int:pk>/like/', MovieLikeCheckView.as_view()),
]
