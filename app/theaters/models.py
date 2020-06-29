from django.db import models


class Theater(models.Model):
    name = models.CharField(max_length=30)
    region = models.ForeignKey(
        'Region',
        related_name='theaters',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.region}/{self.name}'


class Region(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.name}'


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
        'Theater',
        related_name='screens',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.theater} {self.name}'


class Schedule(models.Model):
    movie = models.ForeignKey(
        'movies.Movie',
        related_name='schedules',
        on_delete=models.CASCADE,
    )
    screen = models.ForeignKey(
        'Screen',
        related_name='screens',
        on_delete=models.CASCADE,
    )
    start_time = models.DateTimeField()

    def __str__(self):
        return f'{self.start_time:%m/%d %H:%M} {self.screen} {self.movie}'
