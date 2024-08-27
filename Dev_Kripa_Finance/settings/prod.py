import os
from .base import *

DEBUG = os.environ.get('DEBUG')
ALLOWED_HOSTS = ['3.111.52.245', '*']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_NAME','dev_kripa_stage'),
        'USER': os.environ.get('DB_USER','devKripaStage'),
        'PASSWORD': os.environ.get('DB_PASSWORD','DevKripaFinance'),
        'HOST':os.environ.get('DB_HOST','devkripa-stage.c1moyiyguvhg.ap-south-1.rds.amazonaws.com'),
        'PORT': os.environ.get('DB_PORT','5432')
    }

    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #     'NAME': os.environ.get('DB_NAME','cybite'),
    #     'USER': os.environ.get('DB_USER','postgres'),
    #     'PASSWORD': os.environ.get('DB_PASSWORD','test'),
    #     'HOST':os.environ.get('DB_HOST','localhost'),
    #     'PORT': os.environ.get('DB_PORT','5432')
    # }

    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #     'NAME': os.environ.get('DB_NAME','devKripaInitial'),
    #     'USER': os.environ.get('DB_USER','Dev_admin'),
    #     'PASSWORD': os.environ.get('DB_PASSWORD','DevAdmin-master'),
    #     'HOST':os.environ.get('DB_HOST','dev-kripa-instance.c1moyiyguvhg.ap-south-1.rds.amazonaws.com'),
    #     'PORT': os.environ.get('DB_PORT','5432')
    # }
}

CORS_ALLOW_ALL_ORIGINS = True
