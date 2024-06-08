import os
from .base import *

DEBUG = os.environ.get('DEBUG')
ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_NAME','stage_inital'),
        'USER': os.environ.get('DB_USER','adminStage'),
        'PASSWORD': os.environ.get('DB_PASSWORD','dkFinanceStage'),
        'HOST':os.environ.get('DB_HOST','db-staging.c1moyiyguvhg.ap-south-1.rds.amazonaws.com'),
        'PORT': os.environ.get('DB_PORT','5432')
    }
}