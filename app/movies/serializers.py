from rest_framework import serializers

from utils import reformat_duration
from .models import Movie, Rating, Director, Actor, Genre


class MovieSerializer(serializers.ModelSerializer):
    average_point = serializers.SerializerMethodField('get_average_point')
    acc_favorite = serializers.IntegerField(source='raters.count')

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

    # 성능 부적합. 변경 필요
    def get_average_point(self, movie):
        try:
            ratings = movie.ratings.all()
            points = list()
            for rating in ratings:
                points.append(rating.score)
            average_point = sum(points) / len(points)
            return average_point

        except ZeroDivisionError as e:
            average_point = 0
            return average_point

        except TypeError as e:
            average_point = 0
            return average_point


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
    acc_favorite = serializers.IntegerField(source='raters.all.count')
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

    # 성능 부적합. 변경 필요
    def get_average_point(self, movie):
        try:
            ratings = movie.ratings.all()
            points = list()
            for rating in ratings:
                points.append(rating.score)
            average_point = sum(points) / len(points)
            return average_point

        except ZeroDivisionError as e:
            average_point = 0
            return average_point

        except TypeError as e:
            average_point = 0
            return average_point

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
    teens_sum = serializers.IntegerField()
    twenties_sum = serializers.IntegerField()
    thirties_sum = serializers.IntegerField()
    fourties_sum = serializers.IntegerField()
    fifties_sum = serializers.IntegerField()
