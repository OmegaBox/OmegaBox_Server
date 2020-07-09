from django.urls import path

from .views import MovieListView, MovieDetailView, AgeBookingView

urlpatterns = [
    path('', MovieListView.as_view()),
    path('<int:pk>/', MovieDetailView.as_view()),
    path('<int:pk>/age-booking/', AgeBookingView.as_view()),
]
