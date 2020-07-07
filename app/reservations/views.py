from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from reservations.serializers import SeatGradeCreateSerializer
from theaters.models import SeatGrade


class SeatGradeListCreateView(CreateAPIView):
    queryset = SeatGrade
    serializer_class = SeatGradeCreateSerializer
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        instance = serializer.save()
        instance.reservation.member = self.request.user
        instance.reservation.save()
