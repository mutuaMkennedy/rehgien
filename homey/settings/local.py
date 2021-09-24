from homey.settings.base import *
import os

# python manage.py runserver --settings=homey.settings.local

if os.name == 'nt':
    import platform
    OSGEO4W = r'C:\OSGeo4W'
    if '64' in platform.architecture()[0]:
        OSGEO4W += '64'
    assert os.path.isdir(OSGEO4W), 'Directory does not exist: ' + OSGEO4W
    os.environ['OSGEO4W_ROOT'] = OSGEO4W
    os.environ['GDAL_DATA'] = OSGEO4W + r'\share\gdal'
    os.environ['PROJ_LIB'] = OSGEO4W + r'\share\proj'
    os.environ['PATH'] = OSGEO4W + r'\bin;' + os.environ['PATH']


GDAL_LIBRARY_PATH = r'C:\OSGeo4W64\bin\gdal202.dll'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'rehgienDB',
        'USER': 'postgres',
        'PASSWORD': 'admin$$',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

EMAIL_USE_TLS = False
EMAIL_HOST = "rs2.noc254.com"
EMAIL_HOST_USER = "do-not-reply@rehgien.com"
EMAIL_HOST_PASSWORD = 'donotreply20$$Rehgien'
EMAIL_PORT = 465
EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL = 'Rehgien <do-not-reply@rehgien.com>'

#claudinary settings
cloudinary.config(
  cloud_name = "rehgien",
  api_key = "113141524396467",
  api_secret = "BAsPMg7zobSDbjzPs0yrwnCf-S0"
)

#Initializing Africa's Talking sms Api

africastalking.initialize(
    username='sandbox',
    api_key='1c7c4f43702a67c5100409e323f1aabc98d087a5a590b08239827d988006ab72'
    # username='rehgien',
    # api_key='3e78b952d5fd14a466246eefa2ad8150f866d9adc5afcc14d6ed8d900b41ab63'
)
