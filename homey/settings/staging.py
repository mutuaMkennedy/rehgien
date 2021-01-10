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
