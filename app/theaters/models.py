from django.db import models

from movies.models import Movie


class Theater(models.Model):
    name = models.CharField(max_length=30)
    region = models.ForeignKey(
        'Region',
        related_name='theaters',
        on_delete=models.CASCADE,
    )


class Region(models.Model):
    name = models.CharField(max_length=30)


class Screen(models.Model):
    SCREEN_TYPE_CHOICES = [
        ('A', 'A-type'),
        ('B', 'B-type'),
        ('C', 'C-type'),
    ]
    type = models.CharField(
        max_length=30,
        choices=SCREEN_TYPE_CHOICES,
    )
    name = models.CharField(max_length=30)
    theater = models.ForeignKey(
        Theater,
        related_name='screens',
        on_delete=models.CASCADE,
    )


class Schedule(models.Model):
    movie = models.ForeignKey(
        Movie,
        related_name='schedules',
        on_delete=models.CASCADE,
    )
    screen = models.ForeignKey(
        Screen,
        related_name='screens',
        on_delete=models.CASCADE,
    )
    start_time = models.DateTimeField()
