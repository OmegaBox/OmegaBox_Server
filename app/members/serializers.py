import datetime

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from phonenumber_field.serializerfields import PhoneNumberField
from rest_auth.registration.serializers import RegisterSerializer
from rest_auth.serializers import LoginSerializer as DefaultLoginSerializer
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenRefreshSerializer as DefaultTokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from movies.models import Movie, Rating
from utils.excepts import TakenNumberException, UsernameDuplicateException
from .models import Profile

Member = get_user_model()


class SignUpSerializer(RegisterSerializer):
    name = serializers.CharField()
    email = serializers.EmailField()
    mobile = PhoneNumberField()
    birth_date = serializers.DateField()

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
    reservated_movies_count = serializers.SerializerMethodField('get_reservated_movies_count')
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
            'reservated_movies_count',
            'watched_movies_count',
            'like_movies_count',
            'rating_movies_count',
        ]

    def get_reservated_movies_count(self, member):
        return Movie.objects.filter(
            schedules__reservations__member=member,
            schedules__reservations__payment__isnull=False,
            schedules__start_time__gte=datetime.datetime.today()
        ).distinct().count()

    def get_watched_movies_count(self, member):
        return Movie.objects.filter(
            schedules__reservations__member=member,
            schedules__reservations__payment__isnull=False,
            schedules__start_time__lte=datetime.datetime.today()
        ).distinct().count()

    def get_like_movies_count(self, member):
        return Movie.objects.filter(
            like_members__pk=member.pk,
            movie_likes__liked=True
        ).count()

    def get_rating_movies_count(self, member):
        return Rating.objects.filter(
            member=member
        ).count()
