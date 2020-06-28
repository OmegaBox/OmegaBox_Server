from ._base import *

DEBUG = True

WSGI_APPLICATION = 'config.wsgi.develop.application'

INSTALLED_APPS += [
    'django_extensions',
]

