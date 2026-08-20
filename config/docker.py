# Docker settings
# ruff: noqa: F405
# pyright: reportConstantRedefinition=false
from .settings import *  # noqa: F403

DATABASES: dict[str, DatabaseSettings] = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "pokeapi",
        "USER": "ash",
        "PASSWORD": "pokemon",
        "HOST": "localhost",
        "PORT": "",
    }
}


CACHES: dict[str, CacheSettings] = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

DEBUG = True

for template in TEMPLATES:
    if "OPTIONS" in template and "debug" in template["OPTIONS"]:
        template["OPTIONS"]["debug"] = DEBUG
