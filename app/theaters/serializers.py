from rest_framework import serializers

from .models import Schedule
from .utils import reformat_duration


class ScheduleSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(
        format='%Y-%m-%d',
        source='start_time',
    )
    start_time = serializers.DateTimeField(format='%H:%M')
    running_time = serializers.SerializerMethodField()
    end_time = serializers.SerializerMethodField()
    movie = serializers.CharField(source='movie.name_kor')
    grade = serializers.CharField(source='movie.grade')
    region = serializers.CharField(source='screen.theater.region')
    theater = serializers.CharField(source='screen.theater.name')
    screen = serializers.CharField(source='screen.name')
    screen_type = serializers.CharField(source='screen.screen_type')
    seats_type = serializers.CharField(source='screen.seats_type')
    poster = serializers.ImageField(source='movie.poster')
    grade = serializers.CharField(source='movie.grade')
    region = serializers.CharField(source='screen.theater.region')

    class Meta:
        model = Schedule
        fields = [
            'date',
            'start_time',
            'running_time',
            'end_time',
            'movie',
            'grade',
            'region',
            'theater',
            'screen',
            'screen_type',
            'seats_type',
            'poster',
        ]

    def get_running_time(self, obj):
        return reformat_duration(obj.movie.running_time)

    def get_end_time(self, obj):
        return f'{obj.start_time + obj.movie.running_time:%H:%M}'
