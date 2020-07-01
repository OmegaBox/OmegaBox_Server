from datetime import datetime

from rest_framework.generics import ListAPIView

from .models import Schedule
from .serializers import ScheduleSerializer


class ScheduleList(ListAPIView):
    serializer_class = ScheduleSerializer

    def get_queryset(self):
        date_int = self.kwargs['date']
        theater_id = self.kwargs['theater_id']

        date = datetime.strptime(str(date_int), '%y%m%d')

        queryset = Schedule.objects.filter(
            start_time__gte=date,
            screen__theater_id=theater_id,
        )

        time = self.request.query_params.get('time', None)

        if time is not None:
            time = datetime.strptime(str(time), '%H')
            queryset = queryset.filter(start_time__time__gte=time)
        return queryset
