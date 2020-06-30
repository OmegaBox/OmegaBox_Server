from django.contrib import admin

from .models import Schedule, Screen, Theater, Region, Seat, SeatGrade


@admin.register(Theater)
class TheaterAdmin(admin.ModelAdmin):
    pass


@admin.register(Screen)
class ScreenAdmin(admin.ModelAdmin):
    pass


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    pass


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    pass


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    pass


@admin.register(SeatGrade)
class SeatGradeAdmin(admin.ModelAdmin):
    pass
