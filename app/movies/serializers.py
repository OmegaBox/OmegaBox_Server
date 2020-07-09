from django.db.models import Sum, Count
from rest_framework import serializers

from utils import reformat_duration
from .models import Movie, Rating, Director, Actor, Genre


class MovieSerializer(serializers.ModelSerializer):
    average_point = serializers.SerializerMethodField('get_average_point')
    acc_favorite = serializers.SerializerMethodField('get_acc_favorite')

    class Meta:
        model = Movie
        fields = [
            'id',
            'rank',
            'name_kor',
            'name_eng',
            'poster',
            'description',
            'average_point',
            'grade',
            'reservation_rate',
            'open_date',
            'acc_favorite',
        ]

    def get_average_point(self, movie):
        point_sum = Movie.objects.filter(pk=movie.pk).values('ratings__score').aggregate(
            point_sum=Sum('ratings__score')
        )['point_sum']

        point_count = Movie.objects.filter(pk=movie.pk).values('ratings__score').aggregate(
            point_count=Count('ratings__score')
        )['point_count']

        return point_sum / point_count if point_count != 0 else 0

    def get_acc_favorite(self, movie):
        return movie.raters.filter(ratings__liked=True).count()


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = [
            'name'
        ]


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = [
            'name'
        ]


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = [
            'name'
        ]


class RatingSerializer(serializers.ModelSerializer):
    member = serializers.CharField(source='member.name')
    good_point = serializers.CharField(source='key_point')
    point = serializers.IntegerField(source='score')

    class Meta:
        model = Rating
        fields = [
            'id',
            'member',
            'good_point',
            'point',
            'comment',
            'liked',
        ]


class MovieDetailSerializer(serializers.ModelSerializer):
    average_point = serializers.SerializerMethodField('get_average_point')
    acc_favorite = serializers.SerializerMethodField('get_acc_favorite')
    running_time = serializers.SerializerMethodField()
    directors = DirectorSerializer(many=True)
    actors = ActorSerializer(many=True)
    genres = GenreSerializer(many=True)
    key_point_count = serializers.SerializerMethodField('get_ratings_key_point_count')
    ratings = RatingSerializer(many=True, source='ratings.all')

    class Meta:
        model = Movie
        fields = [
            'id',
            'rank',
            'name_kor',
            'name_eng',
            'poster',
            'trailer',
            'description',
            'average_point',
            'grade',
            'reservation_rate',
            'open_date',
            'close_date',
            'acc_audience',
            'acc_favorite',
            'running_time',
            'directors',
            'actors',
            'genres',
            'key_point_count',
            'ratings',
        ]

    def get_average_point(self, movie):
        point_sum = Movie.objects.filter(pk=movie.pk).values('ratings__score').aggregate(
            point_sum=Sum('ratings__score')
        )['point_sum']

        point_count = Movie.objects.filter(pk=movie.pk).values('ratings__score').aggregate(
            point_count=Count('ratings__score')
        )['point_count']

        return point_sum / point_count if point_count != 0 else 0

    def get_acc_favorite(self, movie):
        return movie.raters.filter(ratings__liked=True).count()

    def get_running_time(self, obj):
        return reformat_duration(obj.running_time)

    def get_ratings_key_point_count(self, movie):
        actor = movie.ratings.filter(key_point='actor').count()
        prod = movie.ratings.filter(key_point='prod').count()
        story = movie.ratings.filter(key_point='story').count()
        visual = movie.ratings.filter(key_point='visual').count()
        ost = movie.ratings.filter(key_point='ost').count()
        return {
            'actors': actor,
            'prods': prod,
            'story': story,
            'visual': visual,
            'ost': ost
        }


class AgeBookingSerializer(serializers.Serializer):
    teens = serializers.IntegerField(source='teens__sum')
    twenties = serializers.IntegerField(source='twenties__sum')
    thirties = serializers.IntegerField(source='thirties__sum')
    fourties = serializers.IntegerField(source='fourties__sum')
    fifties = serializers.IntegerField(source='fifties__sum')
