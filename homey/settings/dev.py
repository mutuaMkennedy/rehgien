from homey.settings.base import *
import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

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

STATICFILES_STORAGE = 'homey.storage.ForgivingManifestStaticFilesStorage'

#claudinary settings
cloudinary.config(
  cloud_name = "rehgien",
  api_key = "113141524396467",
  api_secret = "BAsPMg7zobSDbjzPs0yrwnCf-S0"
)
