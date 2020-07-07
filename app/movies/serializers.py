from rest_framework import serializers

from theaters.models import Schedule
from utils import reformat_duration
from .models import Movie, Rating


class RatingSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='member.name')
    good_point = serializers.CharField(source='key_point')
    point = serializers.IntegerField(source='score')

    class Meta:
        model = Rating
        fields = [
            'id',
            'good_point',
            'point',
            'comment',
        ]


class MovieSerializer(serializers.ModelSerializer):
    running_time = serializers.SerializerMethodField()
    acc_favorite = serializers.SerializerMethodField('get_acc_favorite_from_rating')
    average_point = serializers.SerializerMethodField('get_average_point')
    comments = RatingSerializer(many=True, source='ratings.all')
    liked = serializers.IntegerField(source='liked.all.count')

    class Meta:
        model = Movie
        fields = [
            'id',
            'name_kor',
            'reservation_rate',
            'running_time',
            'rank',
            'grade',
            'acc_audience',
            'acc_favorite',
            'open_date',
            'close_date',
            'description',
            'poster',
            'trailer',
            'comments',
            'liked',
            'average_point',
            # 'age_booking',
        ]

        # depth = 1

    def get_running_time(self, obj):
        return reformat_duration(obj.running_time)

    def get_acc_favorite_from_rating(self, movie):
        acc_favorite = movie.liked.count()
        return acc_favorite

    # 성능 부적합. 변경 필요
    def get_average_point(self, movie):
        try:
            ratings = movie.ratings.all()
            points = list()
            for rating in ratings:
                points = points.append(rating.score)
            average_point = sum(points) / len(points)
            return average_point

        except ZeroDivisionError as e:
            average_point = 0
            return average_point

        except TypeError as e:
            average_point = 0
            return average_point