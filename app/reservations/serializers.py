from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from theaters.models import SeatGrade, Schedule, Seat, SeatType
from utils.excepts import TakenSeatException, InvalidGradeChoicesException, \
    InvalidSeatException
from .models import Reservation


class SeatGradeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeatGrade
        fields = [
            'id',
            'grade',
            'reservation',
        ]
        depth = 1


class SeatGradeCreateSerializer(serializers.Serializer):
    grade = serializers.CharField()
    seat_id = serializers.IntegerField()
    schedule_id = serializers.IntegerField()

    def validate(self, data):
        # grade choice 유효성 검사
        if data['grade'] not in list(zip(*SeatGrade.SEAT_GRADE_CHOICES))[0]:
            raise InvalidGradeChoicesException

        # 이미 예약된 좌석인지 확인
        reservations = Reservation.objects.filter(schedule_id=data['schedule_id'])
        if reservations.exists():
            if reservations.filter(seat_grades__seat__id__contains=data['seat_id']).exists():
                raise TakenSeatException

        # 띄어앉기석인지 확인
        seat_type = get_object_or_404(
            SeatType,
            seat_id=data['seat_id'],
            schedule_id=data['schedule_id']
        )
        if seat_type.type == 'sit_apart':
            raise InvalidSeatException
        return data

    def create(self, validated_data):
        schedule = get_object_or_404(Schedule, pk=validated_data.get('schedule_id'))
        reservation = Reservation.objects.create(schedule=schedule)

        seat = get_object_or_404(Seat, pk=validated_data.get('seat_id'))

        return SeatGrade.objects.create(
            grade=validated_data.get('grade'),
            seat=seat,
            reservation=reservation,
        )

    def to_representation(self, instance):
        return SeatGradeDetailSerializer(instance).data
