from django.urls import path

from .views import ScheduleList

urlpatterns = [
    path('schedule/<int:date>/<int:theater_id>/', ScheduleList.as_view()),
]
