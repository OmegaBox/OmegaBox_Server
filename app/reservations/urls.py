from django.urls import path

from .views import SeatGradeListCreateView

urlpatterns = [
    path('', SeatGradeListCreateView.as_view()),
]
