import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField

from config.settings._base import AUTH_USER_MODEL


class BaseMemberMixin(models.Model):
    name = models.CharField(max_length=30)
    mobile = PhoneNumberField(unique=True)
    birth_date = models.DateField()

    class Meta:
        abstract = True


class Member(AbstractUser, BaseMemberMixin):
    email = models.EmailField(unique=True)

    REQUIRED_FIELDS = ['name', 'email', 'mobile', 'birth_date']

    def __str__(self):
        return f'{self.username} | {self.email}'

    def age(self):
        today = datetime.date.today()
        birth = self.members.birth_date
        age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
        return age


class NonMember(BaseMemberMixin):
    pin_number = models.IntegerField()

    def __str__(self):
        return f'name: {self.name}, mobile: {self.mobile}, birth_date: {self.birth_date}'


class Profile(models.Model):
    TIME_CHOICES = [
        ('00-10', '10시 이전'),
        ('10-13', '10시~13시'),
        ('13-16', '13시~16시'),
        ('16-18', '16시~18시'),
        ('18-21', '18시~21시'),
        ('21-00', '21시 이후'),
    ]

    TIER_CHOICES = [
        ('basic', 'BASIC'),
        ('vip', 'VIP'),
    ]

    member = models.OneToOneField(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    regions = models.ManyToManyField(
        'theaters.Region',
        related_name='profiles',
    )
    genres = models.ManyToManyField(
        'movies.Genre',
        related_name='profiles',
    )
    time = models.CharField(
        max_length=20,
        choices=TIME_CHOICES,
        blank=True,
    )

    tier = models.CharField(
        max_length=20,
        choices=TIER_CHOICES,
        default='basic',
    )

    point = models.PositiveIntegerField(default=0)

    # 프론트와 협의 필요
    is_disabled = models.BooleanField(default=False)


@receiver(post_save, sender=Member)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(member=instance)
