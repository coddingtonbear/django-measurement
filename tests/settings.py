DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django_measurement',
    'tests'
)

SITE_ID = 1
ROOT_URLCONF = 'core.urls'

SECRET_KEY = 'foobar'

USE_L10N = True
