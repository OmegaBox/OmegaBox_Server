from ._base import *

DEBUG = True

WSGI_APPLICATION = 'config.wsgi.develop.application'

INSTALLED_APPS += [
    'django_extensions',
    'debug_toolbar',
]

MIDDLEWARE = [
                 'debug_toolbar.middleware.DebugToolbarMiddleware',
             ] + MIDDLEWARE

ALLOWED_HOSTS += [
    '127.0.0.1',
]

DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": lambda request: True,
}
