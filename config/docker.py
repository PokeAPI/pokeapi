# Docker settings
from .settings import *  # NOQA

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'pokeapi',
            'USER': 'ash',
            'PASSWORD': 'pokemon',
            'HOST': 'localhost',
            'PORT': '',
        }
}

DEBUG = True
TASTYPIE_FULL_DEBUG = True
