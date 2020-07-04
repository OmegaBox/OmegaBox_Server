from django.urls import path

from .views import MovieList

urlpatterns = [
    path('', MovieList.as_view()),
]
