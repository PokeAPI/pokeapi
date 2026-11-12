"""Local development settings for generating the schema against PostgreSQL."""

import os

from .local import *  # noqa: F403

DATABASES: dict[str, DatabaseSettings] = {  # noqa: F405
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB", "pokeapi"),
        "USER": os.environ.get("POSTGRES_USER", "ash"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "pokemon"),
        "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
    }
}
