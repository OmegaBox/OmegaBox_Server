from django.db import models

from config.settings._base import AUTH_USER_MODEL
from members.models import Member
from theaters.models import Screen, Schedule


class Movie(models.Model):
    MOVIE_GRADES = [
        ('all', '전체이용가'),
        ('12+', '12세 이상 관람가'),
        ('15+', '15세 이상 관람'),
        ('18+', '청소년 관람 불가'),
    ]

    liked = models.ManyToManyField(
        Member,
        through='Rating',
        related_name='movies',
    )
    screens = models.ManyToManyField(
        Screen,
        through=Schedule,
        related_name='movies',
    )
    name_kor = models.CharField(max_length=100)
    name_eng = models.CharField(max_length=100)
    code = models.PositiveIntegerField()
    running_time = models.DurationField()
    genre = models.ForeignKey(
        'Genre',
        on_delete=models.CASCADE,
        related_name='movies',
    )
    rank = models.IntegerField(unique=True)
    acc_audience = models.PositiveIntegerField()
    reservation_rate = models.FloatField()
    open_date = models.DateField()
    close_date = models.DateField()
    grade = models.CharField(
        max_length=20,
        choices=MOVIE_GRADES
    )
    description = models.TextField(blank=True)
    poster = models.ImageField(upload_to='posters/', blank=True)
    trailer = models.FileField(upload_to='trailers/', blank=True)

    def __str__(self):
        return f'{self.name_kor} ({self.name_kor})'


class Rating(models.Model):
    KEY_POINT_CHOICES = [
        ('actor', '배우'),
        ('prod', '연출'),
        ('story', '스토리'),
        ('visual', '영상미'),
        ('ost', 'OST'),
    ]
    member = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ratings',
    )
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name='ratings',
    )
    score = models.IntegerField()
    liked = models.BooleanField(default=False)
    key_point = models.CharField(
        max_length=20,
        choices=KEY_POINT_CHOICES,
    )
    comment = models.TextField(blank=True)


class Genre(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.name}'
