from django.urls import path

from .views import MovieListView, AgeBookingCount, MovieDetailView

urlpatterns = [
    path('', MovieListView.as_view()),
    path('<int:pk>/', MovieDetailView.as_view()),
    path('<int:pk>/age_booking/', AgeBookingCount.as_view()),
]
