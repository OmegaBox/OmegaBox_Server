from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from config.settings._base import AUTH_USER_MODEL


class BaseMemberMixin(models.Model):
    name = models.CharField(max_length=30)
    mobile = PhoneNumberField(unique=True)
    birth_date = models.DateField()

    class Meta:
        abstract = True


class Member(AbstractUser, BaseMemberMixin):
    TIER_CHOICES = [
        ('BASIC', 'BASIC'),
        ('VIP', 'VIP'),
    ]

    email = models.EmailField(unique=True)
    tier = models.CharField(
        max_length=20,
        choices=TIER_CHOICES,
        default='BASIC',
    )
    point = models.PositiveIntegerField(default=0)

    REQUIRED_FIELDS = ['email', 'mobile', 'birth_date']

    def __str__(self):
        return f'{self.username} | {self.email}'


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

    member = models.OneToOneField(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    region = models.ManyToManyField(
        'theaters.Region',
        related_name='profiles',
    )
    genre = models.ManyToManyField(
        'movies.Genre',
        related_name='profiles',
    )
    time = models.CharField(
        max_length=20,
        choices=TIME_CHOICES
    )
    # 프론트와 협의 필요
    is_disabled = models.BooleanField(default=False)
