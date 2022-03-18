from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['bwalters89.pythonanywhere.com', 'www.uponyourluck.life', 'uponyourluck.life']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'OPTIONS': {
            'service': 'uponyourluck',
            'passfile': '.my_pgpass',
        },
    }
}


# default static files settings for PythonAnywhere.
# see https://help.pythonanywhere.com/pages/DjangoStaticFiles for more info
MEDIA_ROOT = '/home/bwalters89/UpOnYourLuck/media'
MEDIA_URL = '/media/'
STATIC_ROOT = '/home/bwalters89/UpOnYourLuck/static'
STATIC_URL = '/static/'

TIME_ZONE = 'UTC'

DOMAIN = 'http://uponyourluck.life/'