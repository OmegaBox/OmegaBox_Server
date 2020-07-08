from django.urls import path

from .views import MovieListView, MovieDetailView, AgeBookingCountView

urlpatterns = [
    path('', MovieListView.as_view()),
    path('<int:pk>/', MovieDetailView.as_view()),
    path('<int:pk>/age_booking/', AgeBookingCountView.as_view()),
]
