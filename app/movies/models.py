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

    raters = models.ManyToManyField(
        AUTH_USER_MODEL,
        through='Rating',
        related_name='rating_movies',
    )

    like_members = models.ManyToManyField(
        AUTH_USER_MODEL,
        through='MovieLike',
        related_name='like_movies',
    )

    screens = models.ManyToManyField(
        'theaters.Screen',
        through=Schedule,
        related_name='movies',
    )
    directors = models.ManyToManyField(
        'Director',
        related_name='movies',
    )
    actors = models.ManyToManyField(
        'Actor',
        related_name='movies',
    )
    genres = models.ManyToManyField(
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

    class Meta:
        ordering = ['rank']

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

    # 실제로 영화를 본 member만 생성 가능하도록 예외처리 필요
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
    key_point = models.CharField(
        max_length=20,
        choices=KEY_POINT_CHOICES,
    )
    comment = models.TextField(blank=True)

    # 한줄평 수정 불가능
    created_at = models.DateField(auto_now_add=True)


class MovieLike(models.Model):
    movie = models.ForeignKey(
        'Movie',
        on_delete=models.CASCADE,
        related_name='movie_likes',
    )
    member = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='movie_likes',
    )
    liked = models.BooleanField()

    # liked save 될때마다 갱신
    liked_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.movie, self.member.name


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
