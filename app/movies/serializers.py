import datetime

from rest_framework import serializers

from members.models import BaseMemberMixin
from utils import reformat_duration
from .models import Movie, Rating


# class MovieSerializer(serializers.ModelSerializer):
#     genre = serializers.CharField(source='genre.name')
#     running_time = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Movie
#         fields = [
#             'id',
#             'name_kor',
#             'name_eng',
#             'running_time',
#             'genre',
#             'rank',
#             'acc_audience',
#             'reservation_rate',
#             'open_date',
#             'grade',
#             'description',
#             'poster',
#             'trailer',
#         ]
#
#     def get_running_time(self, obj):
#         return reformat_duration(obj.running_time)


class AgeBookingSerializer(serializers.ModelSerializer):
    teens = serializers.SerializerMethodField('get_age_booking')

    class Meta:
        model = Movie
        fields = [
            'teens',
            # '20',
            # '30',
            # '40',
            # '50'
        ]

    def get_age_booking(self, movie):
        teens = len(BaseMemberMixin.objects.filter(age__lte=9))
        return teens


class MovieSerializer(serializers.ModelSerializer):
    acc_favorite = serializers.SerializerMethodField('get_acc_favorite_from_rating')
    close_date = serializers.SerializerMethodField('get_close_date')
    # age_booking = AgeBookingSerializer()

    class Meta:
        model = Movie
        fields = [
            'name_kor',
            'reservation_rate',
            'rank',
            'acc_audience',
            'acc_favorite',
            'open_date',
            'close_date',
            # 'description',
            # 'age_booking',
            # 'day_booking',
            # 'comments',
        ]

    def get_acc_favorite_from_rating(self, movie):
        acc_favorite = len(movie.liked.all())
        return acc_favorite

    def get_close_date(self, movie):
        close_date = movie.open_date + datetime.timedelta(days=7)
        return close_date
