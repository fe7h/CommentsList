from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-ng%f4rk2=kwu*9q7(d3z!j@syns*!#%8s21uuu_@f3z$(t0788'

DEBUG = True

ALLOWED_HOSTS = []


CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True


CSRF_TRUSTED_ORIGINS = [
    'http://localhost:5173',
]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
