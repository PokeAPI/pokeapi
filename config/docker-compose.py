# Docker settings
from .settings import *  # NOQA

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'pokeapi',
            'USER': 'ash',
            'PASSWORD': 'pokemon',
            'HOST': 'db',
            'PORT': 5432,
        }
}


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://cache:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

DEBUG = False
TASTYPIE_FULL_DEBUG = False
