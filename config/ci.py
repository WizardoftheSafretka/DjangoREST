from .settings import *

DEBUG = False
SECRET_KEY = "django-insecure-ci-test-key"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "test_db",
        "USER": "test_user",
        "PASSWORD": "test_password",
        "HOST": "localhost",
        "PORT": "5432",
    }
}


PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}
