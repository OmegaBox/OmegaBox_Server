from django.urls import path

from .views import ScheduleDetail, ScheduleList

urlpatterns = [
    path('schedule/<int:date>', ScheduleList.as_view()),
    # path('schedule/<int:pk>/', ScheduleDetail.as_view()),
]
