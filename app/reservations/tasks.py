from __future__ import absolute_import, unicode_literals

from datetime import datetime, timedelta

from celery import shared_task

from members.models import Profile
from utils.business_data import POINT_RATE_PER_TIER_CHART
from .models import Reservation, Payment


@shared_task
def delete_unpaid_reservations():
    Reservation.objects.filter(
        payment__isnull=True,
        reserved_at__lte=datetime.now() - timedelta(minutes=10),
    ).delete()


@shared_task
def save_point_for_played_movie():
    _list = Payment.objects.filter(
        is_canceled=False,
        is_point_saved=False,
        reservation__schedule__start_time__lte=datetime.now(),
    ).exclude(
        member__isnull=True
    ).values('member', 'price')

    for _dict in _list:
        profile = Profile.objects.get(member__pk=_dict['member'])
        profile.point += _dict['price'] * POINT_RATE_PER_TIER_CHART[profile.tier]
        profile.save()
