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
        blank=True,
        null=True,
    )
    is_canceled = models.BooleanField(default=False)
    canceled_at = models.DateTimeField(blank=True, null=True)
    code = models.CharField(max_length=20, blank=True, unique=True)

    def __str__(self):
        return f'예약자: {self.member.name} / 상영영화: {self.schedule.movie.name_kor} / 예약코드: {self.code}'


@receiver(post_save, sender=Reservation)
def set_reservation_code(sender, instance, created, **kwargs):
    if created:
        instance.code = get_random_string(length=10) + str(instance.schedule.movie.code)
        instance.save()


class Payment(models.Model):
    PAY_WITH = [
        ('card', '신용/체크카드'),
        ('phone', '휴대폰결제'),
        ('kakao', '카카오페이'),
        ('payco', '페이코'),
    ]

    price = models.PositiveIntegerField()
    discount_price = models.PositiveIntegerField(blank=True, null=True)
    pay_with = models.CharField(choices=PAY_WITH, max_length=30)
    card_name = models.CharField(max_length=30)
    payed_at = models.DateTimeField(auto_now_add=True)
