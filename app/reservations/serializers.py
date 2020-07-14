from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from theaters.models import SeatGrade, Schedule, Seat, SeatType
from utils import (
    calculate_seat_price, verify_receipt_from_bootpay_server, cancel_payment_from_bootpay_server
)
from utils.excepts import (
    TakenSeatException, InvalidGradeChoicesException, InvalidSeatException, PaymentIdReceiptIdNotMatchingException,
    ReservationOwnershipException)
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
            'reservation',
        ]


class PaymentCreateSerializer(serializers.Serializer):
    receipt_id = serializers.CharField()
    price = serializers.IntegerField()
    # discount_price = serializers.IntegerField()
    reservation_id = serializers.IntegerField()

    def validate_reservation_id(self, reservation_id):
        # 본인의 예약인지 확인
        reservation = get_object_or_404(Reservation, pk=reservation_id)
        if reservation.member != self.request.user:
            raise ReservationOwnershipException
        return reservation_id

    def validate(self, data):
        receipt_id = data['receipt_id']
        price = data['price']
        # discount_price = data['discount_price']

        # 실제 결제해야하는 금액과 결제된 금액 확인
        target_price = 0
        # for reservation_id in data['reservations_id']:
        #     reservation = Reservation.objects.get(pk=receipt_id)
        #     screen_type = reservation.schedule.screen.screen_type
        #     grade = reservation.

        result = verify_receipt_from_bootpay_server(receipt_id, price)

        data['pg'] = result['pg']
        data['method'] = result['method']
        if data['method'] == 'card':
            data['card_name'] = result['payment_data']['card_name']
            data['card_num'] = result['payment_data']['card_no']
        data['payed_at'] = result['payment_data']['p_at']
        return data

    def create(self, validated_data):
        reservation_id = validated_data.pop('reservation_id')

        payment = Payment.objects.create(**validated_data)

        Reservation.objects.get(
            pk=reservation_id,
        ).update(
            payment=payment,
        )
        return payment

    def to_representation(self, instance):
        return PaymentDetailSerializer(instance).data


class PaymentCancelSerializer(serializers.Serializer):
    receipt_id = serializers.CharField()
    price = serializers.IntegerField()

    def validate_receipt_id(self, receipt_id):
        if self.instance.receipt_id == receipt_id:
            return receipt_id
        raise PaymentIdReceiptIdNotMatchingException

    def validate(self, data):
        result = cancel_payment_from_bootpay_server(
            receipt_id=data['receipt_id'],
            price=data['price'],
        )
        data['canceled_at'] = result['revoked_at']
        return data

    def update(self, instance, validated_data):
        instance.is_canceled = True
        instance.canceled_at = validated_data['canceled_at']
        instance.save()
        return instance

    def to_representation(self, instance):
        return PaymentDetailSerializer(instance).data
