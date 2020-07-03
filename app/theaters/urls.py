from django.urls import path

from .views import ScheduleList, ScheduleTheaterList, ScheduleRegionCount

urlpatterns = [
    path('schedules/<int:date>/', ScheduleTheaterList.as_view()),
    path('schedules/<int:date>/regions/', ScheduleRegionCount.as_view()),
    path('schedules/<int:date>/<int:theater_id>/', ScheduleList.as_view()),
]
