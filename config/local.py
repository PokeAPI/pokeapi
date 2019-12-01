from .settings import *

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(PROJECT_ROOT, 'db.sqlite3'),
    # }
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'pokeapi_db_typeefficacypast',
        'USER': 'pokeapi',
        'PASSWORD': 'pokeapi',
        'HOST': 'localhost',
        'PORT': '5432',
        'CONN_MAX_AGE': 30
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

DEBUG = True
TASTYPIE_FULL_DEBUG = True
