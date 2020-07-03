from django.db import models


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
        ('A', 'A-type'),
        ('B', 'B-type'),
        ('C', 'C-type'),
    ]
    SCREEN_TYPE_CHOICES = [
        ('2D', '2D'),
        ('2Ds', '2D 자막'),
        ('3D', '3D'),
    ]
    seats_type = models.CharField(
        max_length=20,
        choices=SEATS_TYPE_CHOICES,
        default='A',
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

    def __str__(self):
        return f'{self.start_time:%m/%d %H:%M} {self.screen} {self.movie}'


class Seat(models.Model):
    ROW_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('E', 'E'),
        ('F', 'F'),
        ('G', 'G'),
        ('H', 'H'),
        ('I', 'I'),
    ]
    COL_CHOICES = [(i, i) for i in range(1, 15)]

    # 예매완료좌석은 예매 모델 필드에서 접근
    # 선택불가좌석은 로직제외
    TYPE_CHOICES = [
        ('impossible', '선택불가'),
        ('sit_apart', '띄어앉기석'),
        ('general', '일반'),
        ('disabled', '장애인석'),
    ]

    row = models.CharField(max_length=10, choices=ROW_CHOICES)
    col = models.IntegerField(choices=COL_CHOICES)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    screen = models.ManyToManyField(
        'Screen',
        related_name='seats'
    )
    reservation = models.ManyToManyField(
        'reservations.Reservation',
        through='SeatGrade',
        related_name='seats',
    )


class SeatGrade(models.Model):
    SEAT_GRADE_CHOICES = [
        ('adult', '성인'),
        ('youth', '청소년'),
        ('preferred', '우대')
    ]

    grade = models.CharField(choices=SEAT_GRADE_CHOICES, max_length=10)
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
