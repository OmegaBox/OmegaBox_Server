from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string

from config.settings import AUTH_USER_MODEL


class Reservation(models.Model):
    # member, nonmember MtoM 관계로 변경 검토 필요
    member = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, related_name='members')
    nonmember = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True,
                                  related_name='nonmenbers')

    schedule = models.ForeignKey('theaters.Schedule', on_delete=models.CASCADE)
    payment = models.OneToOneField('Payment', on_delete=models.CASCADE, blank=True, null=True)
    is_canceled = models.BooleanField(default=False)
    canceled_at = models.DateTimeField(blank=True, null=True)
    code = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.schedule


@receiver(post_save, sender='theaters.Schedule')
def reservation_created(sender, instance, created, **kwargs):
    print('created >> ', created)
    if created:
        Reservation.objects.create(schedule=instance, code=get_random_string(length=10))


class Payment(models.Model):
    PAY_WITH = [
        ('card', '신용/체크카드'),
        ('phone', '휴대폰 결제'),
        ('kakao', '카카오페이'),
        ('payco', '페이코'),
    ]

    price = models.PositiveIntegerField()
    pay_with = models.CharField(choices=PAY_WITH, max_length=30)
    card_name = models.CharField(max_length=30)
    payed_at = models.DateTimeField(auto_now_add=True)
