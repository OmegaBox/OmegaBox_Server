from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from members.permissions import IsAuthorizedMember
from theaters.models import SeatGrade
from .models import Payment
from .serializers import SeatGradeCreateSerializer, SeatGradeDetailSerializer, PaymentCreateSerializer, \
    PaymentDetailSerializer


@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_summary='Make Reservation',
    operation_description='영화 좌석 예매 - 결제 전',
    responses={200: SeatGradeDetailSerializer(many=True)}
))
class SeatGradeCreateView(CreateAPIView):
    queryset = SeatGrade.objects.all()
    serializer_class = SeatGradeCreateSerializer
    permission_classes = [IsAuthenticated, ]

    def get_serializer(self, *args, **kwargs):
        kwargs['many'] = True
        return super(SeatGradeCreateView, self).get_serializer(*args, **kwargs)

    def perform_create(self, serializer):
        instance_list = serializer.save()
        for instance in instance_list:
            instance.reservation.member = self.request.user
            instance.reservation.save()


@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_summary='Paying for Reservations',
    operation_description='영화 좌석 예매 - 결제 전',
    responses={201: PaymentDetailSerializer()}
))
class PaymentCreateView(CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentCreateSerializer
    permission_classes = [IsAuthorizedMember, ]
