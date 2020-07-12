from __future__ import absolute_import, unicode_literals

from datetime import datetime, timedelta

from celery import shared_task

from .models import Reservation


@shared_task
def delete_unpaid_reservations():
    Reservation.objects.filter(
        payment__isnull=True,
        reserved_at__lte=datetime.now() - timedelta(minutes=10),
    ).delete()
