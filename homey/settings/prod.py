from homey.settings.base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

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

# Smuggler settings mmore info https://github.com/semente/django-smuggler

# SMUGGLER_EXCLUDE_LIST=
SMUGGLER_FIXTURE_DIR= 'home/mutua/rehgienProject/dbBackups/'
# SMUGGLER_FORMAT=
# SMUGGLER_INDENT=
