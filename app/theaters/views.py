from datetime import datetime

from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView

from .models import Schedule
from .serializers import ScheduleSerializer


class ScheduleList(ListAPIView):
    serializer_class = ScheduleSerializer

    def get_queryset(self):
        date = datetime.strptime(str(self.kwargs['date']), '%y%m%d')
        queryset = Schedule.objects.filter(start_time__gte=date)

        time = self.request.query_params.get('time', None)
        if time is not None:
            time = datetime.strptime(str(time), '%H')
            queryset = queryset.filter(start_time__time__gte=time)
        return queryset


class ScheduleDetail(RetrieveUpdateDestroyAPIView):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
