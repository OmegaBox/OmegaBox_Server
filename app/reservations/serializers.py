from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from theaters.models import SeatGrade, Schedule, Seat, SeatType
from utils import (
    verify_receipt_from_bootpay_server, cancel_payment_from_bootpay_server,
    calculate_seat_price)
from utils.excepts import (
    TakenSeatException, InvalidGradeChoicesException, InvalidSeatException, PaymentIdReceiptIdNotMatchingException,
    ReservationOwnershipException, InvalidScheduleIdException, InvalidSeatIdException, PriceNotMatchingException,
    IncorrectPriceExceptionException)
from .models import Reservation, Payment


class SeatGradeDetailSerializer(serializers.ModelSerializer):
    seat_grade_id = serializers.IntegerField(source='id')
    price = serializers.SerializerMethodField()

    class Meta:
        model = SeatGrade
        fields = [
            'seat_grade_id',
            'grade',
            'seat',
            'price',
        ]

    def get_price(self, obj):
        return calculate_seat_price(
            screen_type=obj.reservation.schedule.screen.screen_type,
            grade=obj.grade,
        )


class ReservationDetailSerializer(serializers.ModelSerializer):
    reservation_id = serializers.IntegerField(source='id')
    seat_grades = SeatGradeDetailSerializer(many=True)

    class Meta:
        model = Reservation
        fields = [
            'reservation_id',
            'member',
            'schedule',
            'payment',
            'reserved_at',
            'seat_grades',
        ]


class ReservationCreateSerializer(serializers.Serializer):
    schedule_id = serializers.IntegerField()
    grades = serializers.ListField(
        child=serializers.CharField()
    )
    seat_ids = serializers.ListField(
        child=serializers.IntegerField()
    )

    def validate_grades(self, grades):
        # grade choice 유효성 검사
        for grade in grades:
            if grade not in list(zip(*SeatGrade.SEAT_GRADE_CHOICES))[0]:
                raise InvalidGradeChoicesException
        return grades

    def validate(self, data):
        # 이미 예약된 좌석인지 확인
        reservations = Reservation.objects.filter(schedule_id=data['schedule_id'])
        if reservations.exists():
            if reservations.filter(seat_grades__seat__id__in=data['seat_ids']).exists():
                raise TakenSeatException

        # 띄어앉기석인지 확인
        if SeatType.objects.filter(
                schedule_id=data['schedule_id'], seat_id__in=data['seat_ids'], type='sit_apart'
        ).exists():
            raise InvalidSeatException

        return data

    def create(self, validated_data):
        try:
            schedule = Schedule.objects.get(pk=validated_data.get('schedule_id'))
        except ObjectDoesNotExist:
            raise InvalidScheduleIdException

        reservation = Reservation.objects.create(schedule=schedule)

        zipped_list = list(zip(validated_data['grades'], validated_data['seat_ids']))

        for _tuple in zipped_list:
            grade = _tuple[0]
            seat_id = _tuple[1]
            try:
                seat = Seat.objects.get(pk=seat_id)
            except ObjectDoesNotExist:
                raise InvalidSeatIdException
            SeatGrade.objects.create(
                grade=grade,
                reservation=reservation,
                seat=seat,
            )
        return reservation

    def to_representation(self, instance):
        return ReservationDetailSerializer(instance).data


class PaymentDetailSerializer(serializers.ModelSerializer):
    payment_id = serializers.IntegerField(source='id')

    class Meta:
        model = Payment
        fields = [
            'payment_id',
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
    discount_price = serializers.IntegerField()
    reservation_id = serializers.IntegerField()

    def validate_reservation_id(self, reservation_id):
        # 본인의 예약인지 확인
        reservation = get_object_or_404(Reservation, pk=reservation_id)
        if reservation.member != self.context['request'].user:
            raise ReservationOwnershipException
        return reservation_id

    def validate(self, data):
        receipt_id = data['receipt_id']
        price = data['price']
        discount_price = data['discount_price']

        # 실제 결제해야하는 금액과 결제된 금액 확인
        target_price = 0
        reservation = Reservation.objects.get(pk=data['reservation_id'])
        screen_type = reservation.schedule.screen.screen_type
        grade_list = reservation.seat_grades.values('grade')
        for grade_dict in grade_list:
            target_price += calculate_seat_price(screen_type, grade_dict['grade'])

        if target_price != price + discount_price:
            raise IncorrectPriceExceptionException

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
        reservation = Reservation.objects.get(pk=reservation_id)
        reservation.payment = payment
        reservation.save()
        return payment

    def to_representation(self, instance):
        return PaymentDetailSerializer(instance).data


class PaymentCancelSerializer(serializers.Serializer):
    receipt_id = serializers.CharField()
    price = serializers.IntegerField()

    def validate_price(self, price):
        if self.instance.price == price:
            return price
        raise PriceNotMatchingException

    def validate_receipt_id(self, receipt_id):
        if self.instance.receipt_id == receipt_id:
            return receipt_id
        raise PaymentIdReceiptIdNotMatchingException

    def validate(self, data):
        # 영화 상영 시간이 지났으면 취소불가하는 로직 추가
        result = cancel_payment_from_bootpay_server(
            receipt_id=data['receipt_id'],
            price=data['price'],
        )
        data['canceled_at'] = result['revoked_at']
        return data

    def update(self, instance, validated_data):
        instance.is_canceled = True
        instance.canceled_at = validated_data['canceled_at']
        instance.reservation.delete()
        instance.save()
        return instance

    def to_representation(self, instance):
        return PaymentDetailSerializer(instance).data
