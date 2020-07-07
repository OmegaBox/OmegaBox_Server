from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from reservations.serializers import SeatGradeCreateSerializer
from theaters.models import SeatGrade


class SeatGradeListCreateView(CreateAPIView):
    queryset = SeatGrade
    permission_classes = [IsAuthenticated, ]

    serializer_class = SeatGradeCreateSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        instance.reservation.member = self.request.user
        instance.reservation.save()
