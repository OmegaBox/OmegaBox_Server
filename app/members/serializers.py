import datetime

from allauth.account import app_settings as allauth_settings
from allauth.account.adapter import get_adapter
from allauth.utils import email_address_exists
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Q
from phonenumber_field.serializerfields import PhoneNumberField
from rest_auth.registration.serializers import RegisterSerializer
from rest_auth.serializers import LoginSerializer as DefaultLoginSerializer
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenRefreshSerializer as DefaultTokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from movies.models import Movie, Rating
from movies.serializers import MovieTimelineSerializer
from reservations.models import Reservation
from utils import reformat_duration
from utils.excepts import TakenNumberException, UsernameDuplicateException, TakenEmailException
from .models import Profile

Member = get_user_model()


class SignUpSerializer(RegisterSerializer):
    name = serializers.CharField()
    email = serializers.EmailField()
    mobile = PhoneNumberField()
    birth_date = serializers.DateField()

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise TakenEmailException
        return email

    def validate_mobile(self, mobile):
        try:
            Member.objects.get(mobile=mobile)
            raise TakenNumberException
        except ObjectDoesNotExist:
            return mobile

    def validate_username(self, username):
        try:
            Member.objects.get(username=username)
            raise UsernameDuplicateException
        except ObjectDoesNotExist:
            return username

    def save(self, request):
        self.is_valid()
        validated_data = self.validated_data
        member = Member.objects.create(
            username=validated_data['username'],
            name=validated_data['name'],
            email=validated_data['email'],
            birth_date=validated_data['birth_date'],
            mobile=validated_data['mobile']
        )
        member.set_password(validated_data.pop('password1'))
        member.save()
        return member


class JWTSerializer(serializers.Serializer):
    refresh = serializers.SerializerMethodField()
    access = serializers.SerializerMethodField()
    id = serializers.IntegerField(source='user.id')
    username = serializers.CharField(source='user.username')
    name = serializers.CharField(source='user.name')
    email = serializers.EmailField(source='user.email')
    birth_date = serializers.DateField(source='user.birth_date')
    mobile = PhoneNumberField(source='user.mobile')

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def get_refresh(self, obj):
        return str(self.get_token(obj['user']))

    def get_access(self, obj):
        return str(self.get_token(obj['user']).access_token)


# for Documentation
class CheckUsernameDuplicateSerializer(serializers.Serializer):
    username = serializers.CharField()


class LoginSerializer(DefaultLoginSerializer):
    username = serializers.CharField(required=True, allow_blank=True)
    email = None


class TokenRefreshResultSerializer(serializers.Serializer):
    access = serializers.CharField()


class TokenRefreshSerializer(DefaultTokenRefreshSerializer):
    def to_representation(self, instance):
        return TokenRefreshResultSerializer(instance).data


class ProfileDetailSerializer(serializers.ModelSerializer):
    regions = serializers.SerializerMethodField('get_regions')
    genres = serializers.SerializerMethodField('get_genres')

    class Meta:
        model = Profile
        fields = [
            'id',
            'tier',
            'point',
            'regions',
            'genres',
            'time',
            'is_disabled',

        ]

    def get_regions(self, profile):
        return [region.name for region in profile.regions.all()]

    def get_genres(self, profile):
        return [genre.name for genre in profile.genres.all()]


class MemberDetailSerializer(serializers.ModelSerializer):
    profile = ProfileDetailSerializer()
    reserved_movies_count = serializers.SerializerMethodField('get_reserved_movies_count')
    watched_movies_count = serializers.SerializerMethodField('get_watched_movies_count')
    like_movies_count = serializers.SerializerMethodField('get_like_movies_count')
    rating_movies_count = serializers.SerializerMethodField('get_rating_movies_count')

    class Meta:
        model = Member
        fields = [
            'id',
            'email',
            'name',
            'mobile',
            'birth_date',
            'profile',
            'reserved_movies_count',
            'watched_movies_count',
            'like_movies_count',
            'rating_movies_count',
        ]

    def get_reserved_movies_count(self, member):
        return Movie.objects.filter(
            schedules__reservations__member=member,
            schedules__reservations__payment__isnull=False,
            schedules__reservations__payment__is_canceled=False,
            schedules__start_time__gt=datetime.datetime.today()
        ).count()

    def get_watched_movies_count(self, member):
        return Movie.objects.filter(
            schedules__reservations__member=member,
            schedules__reservations__payment__isnull=False,
            schedules__reservations__payment__is_canceled=False,
            schedules__start_time__lte=datetime.datetime.today()
        ).count()

    def get_like_movies_count(self, member):
        return Movie.objects.filter(
            like_members__pk=member.pk,
            movie_likes__liked=True
        ).count()

    def get_rating_movies_count(self, member):
        return Rating.objects.filter(
            member=member
        ).count()


class LikeMoviesSerializer(serializers.ModelSerializer):
    movie_name = serializers.CharField(source='name_kor')
    acc_favorite = serializers.SerializerMethodField('get_acc_favorite')
    open_date = serializers.DateField(format='%Y-%m-%d')
    running_time = serializers.SerializerMethodField('get_running_time')
    directors = serializers.SerializerMethodField('get_directors')
    genres = serializers.SerializerMethodField('get_genres')
    liked_at = serializers.SerializerMethodField('get_liked_at')

    class Meta:
        model = Movie
        fields = [
            'movie_name',
            'poster',
            'grade',
            'acc_favorite',
            'open_date',
            'running_time',
            'directors',
            'genres',
            'liked_at',
        ]

    def get_acc_favorite(self, movie):
        return movie.movie_likes.filter(liked=True).count()

    def get_running_time(self, obj):
        return reformat_duration(obj.running_time)

    def get_directors(self, movie):
        return movie.directors.values_list('name', flat=True)

    def get_genres(self, movie):
        return movie.genres.values_list('name', flat=True)

    def get_liked_at(self, movie):
        return movie.movie_likes.get().liked_at


class WatchedMoviesSerializer(serializers.ModelSerializer):
    payment_id = serializers.IntegerField(source='payment.id')
    reservation_code = serializers.CharField(source='payment.code')
    price = serializers.IntegerField(source='payment.price')
    screen_type = serializers.CharField(source='schedule.screen.screen_type')
    screen_name = serializers.CharField(source='schedule.screen.name')
    seat_grade = serializers.SerializerMethodField('get_seat_grade')
    seat_name = serializers.SerializerMethodField('get_seat_name')
    theater_name = serializers.CharField(source='schedule.screen.theater.name')
    theater_region = serializers.CharField(source='schedule.screen.theater.region.name')
    start_time = serializers.DateTimeField(source='schedule.start_time', format='%Y-%m-%d %H:%M')
    payed_at = serializers.DateTimeField(source='payment.payed_at', format='%Y-%m-%d')
    movie = MovieTimelineSerializer(source='schedule.movie')

    class Meta:
        model = Reservation
        fields = [
            'payment_id',
            'reservation_code',
            'price',
            'screen_type',
            'screen_name',
            'seat_grade',
            'seat_name',
            'theater_name',
            'theater_region',
            'start_time',
            'payed_at',
            'movie',
        ]

    def get_seat_grade(self, reservation):
        return reservation.seat_grades.annotate(
            adult=Count('grade', filter=Q(grade='adult')),
            teen=Count('grade', filter=Q(grade='teen')),
            preferential=Count('grade', filter=Q(grade='preferential'))
        ).values('adult', 'teen', 'preferential')

    def get_seat_name(self, reservation):
        return reservation.seats.values_list('name', flat=True)

    def get_acc_favorite(self, reservation):
        return reservation.schedule.movie.movie_likes.filter(liked=True).count()

    def get_running_time(self, obj):
        return reformat_duration(obj.schedule.movie.running_time)

    def get_directors(self, reservation):
        return [director.name for director in reservation.schedule.movie.directors.all()]

    def get_genres(self, reservation):
        return [genre.name for genre in reservation.schedule.movie.genres.all()]


class RatingMoviesSerializer(serializers.ModelSerializer):
    rating_id = serializers.IntegerField(source='id')
    movie = MovieTimelineSerializer()

    class Meta:
        model = Rating
        fields = [
            'rating_id',
            'movie',
            'created_at',
            'score',
            'key_point',
            'comment',
        ]


class ReservedMoviesSerializer(serializers.ModelSerializer):
    reservation_id = serializers.IntegerField(source='id')
    reservation_code = serializers.CharField(source='payment.code')
    price = serializers.IntegerField(source='payment.price')
    movie_name = serializers.CharField(source='schedule.movie.name_kor')
    poster = serializers.ImageField(source='schedule.movie.poster')
    screen_type = serializers.CharField(source='schedule.screen.screen_type')
    screen_name = serializers.CharField(source='schedule.screen.name')
    theater_name = serializers.CharField(source='schedule.screen.theater.name')
    theater_region = serializers.CharField(source='schedule.screen.theater.region.name')
    start_time = serializers.DateTimeField(source='schedule.start_time', format='%Y-%m-%d %H:%M')
    payed_at = serializers.DateTimeField(source='payment.payed_at', format='%Y-%m-%d')
    seat_grade = serializers.SerializerMethodField('get_seat_grade')
    seat_name = serializers.SerializerMethodField('get_seat_name')

    class Meta:
        model = Reservation
        fields = [
            'reservation_id',
            'reservation_code',
            'price',
            'movie_name',
            'poster',
            'screen_type',
            'screen_name',
            'theater_name',
            'theater_region',
            'start_time',
            'seat_grade',
            'seat_name',
            'payed_at',
            # 'prearranged_point',
        ]

    def get_seat_grade(self, reservation):
        return reservation.seat_grades.annotate(
            adult=Count('grade', filter=Q(grade='adult')),
            teen=Count('grade', filter=Q(grade='teen')),
            preferential=Count('grade', filter=Q(grade='preferential'))
        ).values('adult', 'teen', 'preferential')

    def get_seat_name(self, reservation):
        return reservation.seats.values_list('name', flat=True)


class CanceledReservationMoviesSerializer(serializers.ModelSerializer):
    reservation_id = serializers.IntegerField(source='id')
    canceled_at = serializers.DateTimeField(source='payment.canceled_at', format='%Y-%m-%d %H:%M')
    movie_name = serializers.CharField(source='schedule.movie.name_kor')
    theater_name = serializers.CharField(source='schedule.screen.theater.name')
    theater_region = serializers.CharField(source='schedule.screen.theater.region.name')
    start_time = serializers.DateTimeField(source='schedule.start_time', format='%Y-%m-%d %H:%M')
    canceled_payment = serializers.IntegerField(source='payment.price')

    class Meta:
        model = Reservation
        fields = [
            'reservation_id',
            'canceled_at',
            'movie_name',
            'theater_name',
            'theater_region',
            'start_time',
            'canceled_payment',
        ]
