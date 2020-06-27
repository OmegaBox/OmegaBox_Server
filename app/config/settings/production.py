from ._base import *

DEBUG = False

WSGI_APPLICATION = 'config.wsgi.production.application'

ALLOWED_HOSTS += ['*']
