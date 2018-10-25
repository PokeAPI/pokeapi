from .settings import *

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(PROJECT_ROOT, 'db.sqlite3'),
    # },
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'pokeapi',
        'USER': 'root',
        'PASSWORD': 'pokeapi',
        'HOST': 'localhost',
        'PORT': '',
        'CONN_MAX_AGE': 30
    },
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

DEBUG = True
TASTYPIE_FULL_DEBUG = True

LOGGING = {
    'version': 1,
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        'config.middleware': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    }
}

MIDDLEWARE = [
    # Log each database SQL query to the console for debugging
    # 'config.middleware.QueryDebugMiddleware',

    # Log the number of queries and the total run time to the console
    'config.middleware.QueryCountDebugMiddleware'
] + MIDDLEWARE
