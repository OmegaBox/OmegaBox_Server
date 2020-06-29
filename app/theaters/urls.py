from django.urls import path

from .views import ScheduleDetail

urlpatterns = [
    path('schedule/<int:pk>/', ScheduleDetail.as_view()),
]
