from django.urls import path

from .views import MovieList, AgeBookingList

urlpatterns = [
    path('', MovieList.as_view()),
    path('age/', AgeBookingList.as_view()),
]
