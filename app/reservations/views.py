from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from reservations.serializers import SeatGradeCreateSerializer, SeatGradeDetailSerializer
from theaters.models import SeatGrade


@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_summary='Make Reservation',
    operation_description='영화 좌석 예매 - 결제 전',
    responses={200: SeatGradeDetailSerializer()}
))
class SeatGradeCreateView(CreateAPIView):
    queryset = SeatGrade
    serializer_class = SeatGradeCreateSerializer
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        instance = serializer.save()
        instance.reservation.member = self.request.user
        instance.reservation.save()
