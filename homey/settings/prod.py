from homey.settings.base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'homeydb',
        'USER': 'admin',
        'PASSWORD': 'dbadmin20$$',
        'HOST': 'localhost',
        'PORT': '',
    }
}

STATICFILES_STORAGE = 'homey.storage.ForgivingManifestStaticFilesStorage'
