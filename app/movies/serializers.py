from rest_framework import serializers

from utils import reformat_duration
from .models import Movie


class MovieSerializer(serializers.ModelSerializer):
    genre = serializers.CharField(source='genre.name')
    running_time = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = [
            'id',
            'name_kor',
            'name_eng',
            'running_time',
            'genre',
            'rank',
            'acc_audience',
            'reservation_rate',
            'open_date',
            'grade',
            'description',
            'poster',
            'trailer',
        ]

    def get_running_time(self, obj):
        return reformat_duration(obj.running_time)
