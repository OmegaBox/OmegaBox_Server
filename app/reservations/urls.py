from django.urls import path

from .views import SeatGradeCreateView

urlpatterns = [
    path('', SeatGradeCreateView.as_view()),
]
