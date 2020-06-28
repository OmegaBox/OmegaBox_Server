from django.contrib import admin

from .models import Movie, Genre


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    pass


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass
