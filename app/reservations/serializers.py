from django.db.models import Count, Q
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from movies.serializers import MovieTimelineSerializer
from theaters.models import SeatGrade, Schedule, Seat, SeatType
from utils import calculate_seat_price, verify_receipt_from_bootpay_server, reformat_duration
from utils.excepts import TakenSeatException, InvalidGradeChoicesException, \
    InvalidSeatException
from .models import Reservation, Payment


class ReservationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = [
            'id',
            'member',
            'schedule',
            'payment',
        ]


class SeatGradeDetailSerializer(serializers.ModelSerializer):
    reservation = ReservationDetailSerializer()
    price = serializers.SerializerMethodField()

    class Meta:
        model = SeatGrade
        fields = [
            'id',
            'grade',
            'price',
            'reservation',
        ]

    def get_price(self, obj):
        return calculate_seat_price(
            screen_type=obj.reservation.schedule.screen.screen_type,
            grade=obj.grade,
        )


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


class PaymentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            'id',
            'code',
            'receipt_id',
            'price',
            'discount_price',
            'pg',
            'method',
            'card_name',
            'card_num',
            'payed_at',
            'is_canceled',
            'canceled_at',
            'reservations',
        ]


class PaymentCreateSerializer(serializers.Serializer):
    receipt_id = serializers.CharField()
    price = serializers.IntegerField()
    reservations_id = serializers.ListField(
        child=serializers.IntegerField()
    )

    def validate(self, data):
        receipt_id = data['receipt_id']
        price = data['price']

        result = verify_receipt_from_bootpay_server(receipt_id, price)

        data['pg'] = result['pg']
        data['method'] = result['method']
        if data['method'] == 'card':
            data['card_name'] = result['payment_data']['card_name']
            data['card_num'] = result['payment_data']['card_no']
        data['payed_at'] = result['payment_data']['p_at']
        return data

    def create(self, validated_data):
        reservations_id = validated_data.pop('reservations_id')

        payment = Payment.objects.create(**validated_data)

        # 예매의 총합 금액과 결제 금액 검증 로직 필요
        Reservation.objects.filter(
            id__in=reservations_id,
        ).update(
            payment=payment,
        )
        return payment

    def to_representation(self, instance):
        return PaymentDetailSerializer(instance).data
