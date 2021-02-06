# Production settings
import os
from unipath import Path

PROJECT_ROOT = Path(__file__).ancestor(2)

DEBUG = False

TEMPLATE_DEBUG = DEBUG

ADMINS = (("Paul Hallett", "paulandrewhallett@gmail.com"),)

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

MANAGERS = ADMINS

BASE_URL = "http://pokeapi.co"

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [".pokeapi.co", "localhost", "127.0.0.1"]

TIME_ZONE = "Europe/London"

LANGUAGE_CODE = "en-gb"

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Explicitly define test runner to avoid warning messages on test execution
TEST_RUNNER = "django.test.runner.DiscoverRunner"

SECRET_KEY = "4nksdock439320df*(^x2_scm-o$*py3e@-awu-n^hipkm%2l$sw$&2l#"

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "pokeapi_co_db",
        "USER": "root",
        "PASSWORD": "pokeapi",
        "HOST": "localhost",
        "PORT": "",
        "CONN_MAX_AGE": 30,
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient",},
    }
}

SECRET_KEY = os.environ.get(
    "SECRET_KEY", "ubx+22!jbo(^x2_scm-o$*py3e@-awu-n^hipkm%2l$sw$&2l#"
)

CUSTOM_APPS = (
    "tastypie",
    "pokemon_v2",
)

INSTALLED_APPS = (
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.admin",
    "django.contrib.humanize",
    "corsheaders",
    "rest_framework",
    "cachalot",
) + CUSTOM_APPS


API_LIMIT_PER_PAGE = 1

TASTYPIE_DEFAULT_FORMATS = ["json"]

CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_METHODS = "GET"

CORS_URLS_REGEX = r"^/api/.*$"

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": ("drf_ujson.renderers.UJSONRenderer",),
    "DEFAULT_PARSER_CLASSES": ("drf_ujson.renderers.UJSONRenderer",),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 20,
    "PAGINATE_BY": 20,
}
