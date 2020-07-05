from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from phonenumber_field.serializerfields import PhoneNumberField
from rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from utils.excepts import TakenNumberException
from .models import Profile

Member = get_user_model()


class SignUpSerializer(RegisterSerializer):
    name = serializers.CharField()
    mobile = PhoneNumberField()
    birth_date = serializers.DateField()

    def validate_mobile(self, mobile):
        try:
            Member.objects.get(mobile=mobile)
            raise TakenNumberException
        except ObjectDoesNotExist:
            return mobile

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


class ProfileDetailSerializer(serializers.ModelSerializer):
    tier = serializers.CharField(source='member.tier')
    point = serializers.CharField(source='member.point')

    class Meta:
        model = Profile
        fields = '__all__'
