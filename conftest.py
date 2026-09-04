"""Make ``pytest`` work the same way ``manage.py test`` does.

The Django test cases in ``pokemon_v2`` import the models at module level and
need a configured settings module plus a migrated test database. Django's own
runner (``make test``) sets both up; this file does the equivalent for a bare
``pytest`` run so the suite can be collected and executed without pytest-django.
"""

import os
from typing import TYPE_CHECKING

import django
import pytest
from django.test.utils import (
    setup_databases,
    setup_test_environment,
    teardown_databases,
    teardown_test_environment,
)

if TYPE_CHECKING:
    from collections.abc import Iterator

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.local")
django.setup()


@pytest.fixture(scope="session", autouse=True)
def _django_test_database(request: pytest.FixtureRequest) -> "Iterator[None]":
    if request.config.pluginmanager.hasplugin("django"):
        # pytest-django is installed and manages the test database itself.
        yield
        return
    setup_test_environment()
    old_config = setup_databases(verbosity=0, interactive=False)
    try:
        yield
    finally:
        teardown_databases(old_config, verbosity=0)
        teardown_test_environment()
