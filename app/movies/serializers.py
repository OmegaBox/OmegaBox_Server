from rest_framework import serializers

from .models import Movie


class MovieSerializer(serializers.ModelSerializer):
    genre = serializers.CharField(source='genre.name')

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
            'close_date',
            'grade',
            'description',
            'poster',
            'trailer',
        ]
