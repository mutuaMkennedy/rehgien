from homey.settings.base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'rehgienTestDb',
        'USER': 'rehgienAdmin ',
        'PASSWORD': 'admin20$$',
        'HOST': 'localhost',
        'PORT': '5412',
    }
}

STATICFILES_STORAGE = 'homey.storage.ForgivingManifestStaticFilesStorage'

#claudinary settings
cloudinary.config(
  cloud_name = "rehgien",
  api_key = "113141524396467",
  api_secret = "BAsPMg7zobSDbjzPs0yrwnCf-S0"
)
