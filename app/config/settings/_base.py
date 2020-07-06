"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 2.2.13.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""
import json
import os
from datetime import timedelta

import boto3
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = os.path.dirname(BASE_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# AWS_SECRETS_MANAGER
AWS_SECRETS_MANAGER_SECRET_NAME = 'CaloCulator'
AWS_SECRETS_MANAGER_PROFILE = 'CaloCulator'
AWS_SECRETS_MANAGER_REGION_NAME = 'ap-northeast-2'

session = boto3.session.Session(
    profile_name=AWS_SECRETS_MANAGER_PROFILE,
    region_name=AWS_SECRETS_MANAGER_REGION_NAME,
)
client = session.client(
    service_name='secretsmanager',
    region_name=AWS_SECRETS_MANAGER_REGION_NAME,
)

SECRETS_STRING = client.get_secret_value(SecretId=AWS_SECRETS_MANAGER_SECRET_NAME)['SecretString']
SECRETS = json.loads(SECRETS_STRING)

# S3
AWS_STORAGE_BUCKET_NAME = SECRETS['AWS_STORAGE_BUCKET_NAME']
AWS_S3_REGION_NAME = 'ap-northeast-2'
AWS_DEFAULT_ACL = None

AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com'

# s3 static settings
STATIC_LOCATION = 'static'
STATICFILES_STORAGE = 'config.storages.S3StaticStorage'
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/'

# s3 media settings
DEFAULT_FILE_STORAGE = 'config.storages.S3MediaStorage'
MEDIA_LOCATION = 'media'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{MEDIA_LOCATION}/'

# STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'), ]

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = SECRETS['DJANGO_SECRET_KEY']

ALLOWED_HOSTS = []

AUTH_USER_MODEL = 'members.Member'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # 3rd-party packages
    'allauth',
    'allauth.account',
    'rest_auth',
    'rest_auth.registration',

    'rest_framework',
    'rest_framework.authtoken',

    'drf_yasg',

    'phonenumber_field',

    # Local
    'members.apps.MembersConfig',
    'movies.apps.MoviesConfig',
    'theaters.apps.TheatersConfig',
    'reservations.apps.ReservationsConfig',
]

# Django allauth
SITE_ID = 1
ACCOUNT_EMAIL_VERIFICATION = None

# Application definition

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(ROOT_DIR, 'db.sqlite3'),
#     }
# }

DATABASES = SECRETS['DATABASES']

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

# django-phonenumber-field
PHONENUMBER_DEFAULT_REGION = 'KR'
PHONENUMBER_DB_FORMAT = 'NATIONAL'

# DRF
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ]
}

# DJANGO_REST_AUTH
REST_USE_JWT = True
REST_AUTH_SERIALIZERS = {
    'JWT_SERIALIZER': 'members.serializers.JWTSerializer',
}

REST_AUTH_REGISTER_SERIALIZERS = {
    'REGISTER_SERIALIZER': 'members.serializers.SignUpSerializer',
}

# DJANGO_SIMPLE_JWT
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
}

# Sentry
sentry_sdk.init(
    dsn="https://b90073877e834c63ab9b60864c1c470c@o415300.ingest.sentry.io/5306171",
    integrations=[DjangoIntegration()],

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)
