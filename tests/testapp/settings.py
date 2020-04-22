DEBUG = True

INSTALLED_APPS = (
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.auth",
    "django.contrib.messages",
    "django.contrib.admin",
    "django.contrib.staticfiles",
    "django_measurement",
    "tests.testapp",
)

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

DATABASES = {"default": {"ENGINE": "django.db.backends.postgresql", "NAME": "measurement"}}

ROOT_URLCONF = "tests.testapp.urls"

SECRET_KEY = "foobar"

STATIC_URL = '/static/'

USE_L10N = True

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.template.context_processors.i18n",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "debug": DEBUG,
        },
    },
]
