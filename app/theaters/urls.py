from django.urls import path

from .views import ScheduleList, ScheduleTheaterList, ScheduleRegionCount, SeatList

urlpatterns = [
    path('schedules/<int:date>/', ScheduleTheaterList.as_view()),
    path('schedules/regions/<int:date>/', ScheduleRegionCount.as_view()),
    path('<int:theater_id>/schedules/<int:date>/', ScheduleList.as_view()),

    path('schedules/<int:schedule_id>/seats/', SeatList.as_view()),
]
