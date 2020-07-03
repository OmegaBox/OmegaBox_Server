from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from utils.omegabox_data import seating_chart


class Theater(models.Model):
    name = models.CharField(max_length=30)
    region = models.ForeignKey(
        'Region',
        related_name='theaters',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.name} ({self.region})'


class Region(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.name}'


class Screen(models.Model):
    SEATS_TYPE_CHOICES = [
        ('0', 'type_0'),
        ('1', 'type_1'),
        ('2', 'type_2'),
    ]
    SCREEN_TYPE_CHOICES = [
        ('2D', '2D'),
        ('2Ds', '2D 자막'),
        ('3D', '3D'),
    ]
    seats_type = models.CharField(
        max_length=20,
        choices=SEATS_TYPE_CHOICES,
        default='0',
    )
    screen_type = models.CharField(
        max_length=20,
        choices=SCREEN_TYPE_CHOICES,
        default='2D',
    )
    name = models.CharField(max_length=30)
    theater = models.ForeignKey(
        'Theater',
        related_name='screens',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.theater} {self.name}'


@receiver(post_save, sender=Screen)
def create_seats(sender, instance, created, **kwargs):
    if created:
        type_number = instance.seats_type
        seats_list = seating_chart.get(type_number, None)

        if seats_list is not None:
            for seat in seats_list:
                seat_instance = Seat.objects.get(name=seat)

                SeatType.objects.create(
                    seat=seat_instance,
                    screen=instance,
                )


class Schedule(models.Model):
    movie = models.ForeignKey(
        'movies.Movie',
        related_name='schedules',
        on_delete=models.CASCADE,
    )
    screen = models.ForeignKey(
        'Screen',
        related_name='schedules',
        on_delete=models.CASCADE,
    )
    start_time = models.DateTimeField()

    class Meta:
        ordering = ['start_time']

    def __str__(self):
        return f'{self.start_time:%m/%d %H:%M} {self.screen} {self.movie}'


class Seat(models.Model):
    name = models.CharField(max_length=20)
    screen = models.ManyToManyField(
        'Screen',
        through='SeatType',
        related_name='seats',
    )
    reservation = models.ManyToManyField(
        'reservations.Reservation',
        through='SeatGrade',
        related_name='seats',
    )

    def __str__(self):
        return f'{self.name}'


class SeatType(models.Model):
    # 예매완료좌석은 예매 모델 필드에서 접근
    # 선택불가좌석은 로직제외
    TYPE_CHOICES = [
        ('impossible', '선택불가'),
        ('sit_apart', '띄어앉기석'),
        ('general', '일반'),
        ('disabled', '장애인석'),
    ]
    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default='general',
    )
    seat = models.ForeignKey(
        'Seat',
        on_delete=models.CASCADE,
        related_name='seat_types',
    )
    screen = models.ForeignKey(
        'Screen',
        on_delete=models.CASCADE,
        related_name='seat_types',
    )


class SeatGrade(models.Model):
    SEAT_GRADE_CHOICES = [
        ('adult', '성인'),
        ('youth', '청소년'),
        ('preferred', '우대')
    ]

    grade = models.CharField(
        choices=SEAT_GRADE_CHOICES,
        max_length=10,
        default='adult',
    )
    seat = models.ForeignKey(
        'Seat',
        on_delete=models.CASCADE,
        related_name='seat_grades',
    )
    reservation = models.ForeignKey(
        'reservations.Reservation',
        on_delete=models.CASCADE,
        related_name='seat_grades',
    )
