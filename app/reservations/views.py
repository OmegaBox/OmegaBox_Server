from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import CreateAPIView, GenericAPIView, DestroyAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated

from utils.excepts import InvalidReservationIdException
from .models import Payment, Reservation
from .serializers import (
    PaymentCreateSerializer, PaymentDetailSerializer, PaymentCancelSerializer, ReservationCreateSerializer,
    ReservationDetailSerializer,
    ReservationDeleteSerializer)


@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_summary='Make Reservation',
    operation_description='영화 좌석 예매 (결제 전) - 10분 이내에 미결제 시 자동 삭제',
    responses={201: ReservationDetailSerializer()}
))
class ReservationCreateView(CreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationCreateSerializer
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        instance = serializer.save()
        instance.member = self.request.user
        instance.save()


class ReservationDeleteView(DestroyAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationDeleteSerializer
    permission_classes = [IsAuthenticated, ]

    def get_object(self):
        try:
            reservation = Reservation.objects.get(
                pk=self.kwargs['reservation_id'],
                member=self.request.user,
                payment__isnull=True,
            )
        except ObjectDoesNotExist:
            raise InvalidReservationIdException
        return reservation


@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_summary='Paying for Reservations',
    operation_description='예매 좌석들 결제',
    responses={201: PaymentDetailSerializer()}
))
class PaymentCreateView(CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentCreateSerializer

    def perform_create(self, serializer):
        serializer.save(member=self.request.user)


@method_decorator(name='put', decorator=swagger_auto_schema(
    operation_summary='Cancel Payments',
    operation_description='결제 취소',
    responses={200: PaymentDetailSerializer()}
))
class PaymentCancelView(UpdateModelMixin, GenericAPIView):
    serializer_class = PaymentCancelSerializer

    def get_object(self):
        return Payment.objects.get(
            pk=self.kwargs['pk'],
            member=self.request.user
        )

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
