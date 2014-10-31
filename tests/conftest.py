import os
from django import conf


def pytest_configure():
    os.environ[conf.ENVIRONMENT_VARIABLE] = "tests.settings"

    try:
        import django
        django.setup()
    except AttributeError:
        pass

    from django.test.utils import setup_test_environment

    setup_test_environment()

    from django.db import connection

    connection.creation.create_test_db()
