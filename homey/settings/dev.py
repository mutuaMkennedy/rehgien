from homey.settings.base import *
import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'rehgiendb',
        'USER':'admin',
        'PASSWORD': 'admin$$',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

STATICFILES_STORAGE = 'django_forgiving_collecstatic.storages.ForgivingManifestStaticFilesStorage'
