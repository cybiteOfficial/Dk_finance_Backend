import os
from .base import *

DEBUG = os.environ.get('DEBUG')
ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_NAME','dk_finance_local'),
        'USER': os.environ.get('DB_USER','postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD','postgres'),
        'HOST':os.environ.get('DB_HOST','localhost'),
        'PORT': os.environ.get('DB_PORT','5432')
    }
}