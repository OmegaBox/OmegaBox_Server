from rest_framework.generics import RetrieveUpdateDestroyAPIView

from .models import Schedule
from .serializers import ScheduleSerializer


class ScheduleDetail(RetrieveUpdateDestroyAPIView):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
