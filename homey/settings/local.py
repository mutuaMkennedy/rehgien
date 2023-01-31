import cloudinary
import cloudinary.uploader
import cloudinary.api
from homey.settings.base import *
from glob import glob

GDAL_LIBRARY_PATH=glob('/usr/lib/libgdal.so.*')[0]
GEOS_LIBRARY_PATH=glob('/usr/lib/libgeos_c.so.*')[0]

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}

EMAIL_USE_TLS = config('EMAIL_USE_TLS',cast=bool)
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_USE_SSL = config('EMAIL_USE_SSL', cast=bool)
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')

#cloudinary settings
cloudinary.config(
  cloud_name = config('CLOUD_NAME'),
  api_key = config('API_KEY'),
  api_secret = config('API_SECRET')
)


#Initializing Africa's Talking sms Api
# africastalking.initialize(
#     username=config("AFT_USERNAME"),
#     api_key=config('AFT_API_KEY')
# )


# Twilio settings
TWILIO_CONVERSATIONS_SERVICE_SID = config("TWILIO_CONVERSATIONS_SERVICE_SID")
TWILIO_MESSAGING_SERVICE_SID = config("TWILIO_MESSAGING_SERVICE_SID")
TWILIO_PHONE_NUMBER = config("TWILIO_PHONE_NUMBER")

# M-pesa daraja settings
CONSUMER_KEY = config("CONSUMER_KEY")
CONSUMER_SECRET = config("CONSUMER_SECRET")
ACCESS_TOKEN_API_ENDPOINT = config("ACCESS_TOKEN_API_ENDPOINT")
REGISTER_URL_API_ENDPOINT = config("REGISTER_URL_API_ENDPOINT")
MPESA_EXPRESS_API_ENDPOINT = config("MPESA_EXPRESS_API_ENDPOINT")
MPESA_B2C_API_ENDPOINT = config("MPESA_B2C_API_ENDPOINT")