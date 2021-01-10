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
