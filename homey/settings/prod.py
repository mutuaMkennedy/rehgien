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

#claudinary settings
cloudinary.config(
  cloud_name = "rehgien-inc",
  api_key = "435726737312679",
  api_secret = "0ULgyGJ9Mj77dbIO5vrbrfB_NFY"
)
