from django.urls import path, include

from .views import MovieList

urlpatterns = [
    path('', MovieList.as_view()),
    # path('', include('youtube_download.urls')),
]
