# pyright: reportConstantRedefinition=false
# ruff: noqa: F405
from .settings import *  # noqa: F403

DATABASES: dict[str, DatabaseSettings] = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

CACHES: dict[str, CacheSettings] = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}

DEBUG = True

for template in TEMPLATES:
    if "OPTIONS" in template and "debug" in template["OPTIONS"]:
        template["OPTIONS"]["debug"] = DEBUG
