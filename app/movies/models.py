from django.db import models

from config.settings._base import AUTH_USER_MODEL
from theaters.models import Schedule


class Movie(models.Model):
    MOVIE_GRADES = [
        ('all', '전체관람가'),
        ('12+', '12세이상관람가'),
        ('15+', '15세이상관람가'),
        ('18+', '청소년관람불가'),
    ]

    liked = models.ManyToManyField(
        AUTH_USER_MODEL,
        through='Rating',
        related_name='movies',
    )
    screens = models.ManyToManyField(
        'theaters.Screen',
        through=Schedule,
        related_name='movies',
    )
    director = models.ManyToManyField(
        'Director',
        related_name='movies',
    )
    actor = models.ManyToManyField(
        'Actor',
        related_name='movies',
    )
    genre = models.ManyToManyField(
        'Genre',
        related_name='movies',
    )
    name_kor = models.CharField(max_length=100)
    name_eng = models.CharField(max_length=100)
    code = models.PositiveIntegerField()
    running_time = models.DurationField(help_text='<분:초>로 입력 - 예시: 90:00 (90분)')
    rank = models.IntegerField(unique=True)
    acc_audience = models.PositiveIntegerField()
    reservation_rate = models.FloatField()
    open_date = models.DateField()
    close_date = models.DateField(
        default='2020-08-31',
    )
    grade = models.CharField(
        max_length=20,
        choices=MOVIE_GRADES,
    )
    description = models.TextField(blank=True)
    poster = models.ImageField(upload_to='posters/', blank=True)
    trailer = models.FileField(upload_to='trailers/', blank=True)

    def __str__(self):
        return f'{self.rank}위: {self.name_kor} ({self.name_eng})'


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
        'Movie',
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


class NameObject(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.name}'


class Genre(NameObject):
    pass


class Director(NameObject):
    pass


class Actor(NameObject):
    pass
