from django.urls import path

from .views import (
    ScheduleListGivenDate, TheatersGivenDateList, TheatersRegionCountGivenDate, ReservedSeatList, ScreenDetail,
    TotalAndReservedSeatsCount, SeatsTotalPrice)

urlpatterns = [
    path('schedules/regions/<int:date>/', TheatersRegionCountGivenDate.as_view()),
    path('schedules/<int:date>/', TheatersGivenDateList.as_view()),
    path('schedules/<int:schedule_id>/price/', SeatsTotalPrice.as_view()),
    path('schedules/<int:schedule_id>/reserved-seats/', ReservedSeatList.as_view()),
    path('schedules/<int:schedule_id>/seats/count/', TotalAndReservedSeatsCount.as_view()),
    path('screens/<int:screen_id>/', ScreenDetail.as_view()),
    path('<int:theater_id>/schedules/<int:date>/', ScheduleListGivenDate.as_view()),

]
