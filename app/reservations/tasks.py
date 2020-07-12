from __future__ import absolute_import, unicode_literals

from celery import shared_task


@shared_task
def delete_unpaid_reservations():
    print("reservations deleted!")
