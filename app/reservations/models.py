import random
from datetime import datetime

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string

from config.settings._base import AUTH_USER_MODEL


class Reservation(models.Model):
    member = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='reservations',
    )
    nonmember = models.ForeignKey(
        'members.NonMember',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='reservations',
    )
    schedule = models.ForeignKey(
        'theaters.Schedule',
        on_delete=models.CASCADE,
        related_name='reservations',
    )
    payment = models.OneToOneField(
        'Payment',
        on_delete=models.CASCADE,
        related_name='reservation',
        blank=True,
        null=True,
    )
    reserved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.pk}, 예약자: {self.member.name}({self.member.pk}) / 상영영화: {self.schedule.movie.name_kor}'


class Payment(models.Model):
    PG_CHOICES = [
        ('payletter', '페이레터'),
        ('kakao', '카카오페이'),
    ]
    METHOD_CHOICES = [
        ('card', '카드결제'),
        ('easy', '간편결제'),
    ]
    member = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    code = models.CharField(max_length=50)
    receipt_id = models.CharField(max_length=50)
    price = models.PositiveIntegerField()
    discount_price = models.PositiveIntegerField(blank=True, null=True)
    pg = models.CharField(max_length=20, choices=PG_CHOICES)
    method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    card_name = models.CharField(max_length=30, blank=True)
    card_num = models.PositiveIntegerField(blank=True, null=True)
    payed_at = models.DateTimeField(auto_now_add=True)
    is_canceled = models.BooleanField(default=False)
    canceled_at = models.DateTimeField(auto_now=True)
    is_point_saved = models.BooleanField(default=False)


@receiver(post_save, sender=Payment)
def set_payment_code(sender, instance, created, **kwargs):
    if created:
        date = datetime.now().strftime("%y%m%d")
        random_string = get_random_string(length=2, allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        random_number = random.randint(1000, 9999)
        instance.code = f'{date}-{random_string}-{str(random_number)}'
        instance.save()
