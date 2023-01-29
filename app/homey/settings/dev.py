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

# Twilio settings
TWILIO_CONVERSATIONS_SERVICE_SID = 'ISea7dbadbee2b4c80b87b2459211ca4ab'
TWILIO_MESSAGING_SERVICE_SID = ''
TWILIO_PHONE_NUMBER = ''

# M-pesa daraja settings
CONSUMER_KEY = "EiXmkNt4ha8TEFbGvmMuC7cm6mGRhR8p"
CONSUMER_SECRET = 'zaxeviE8GB7GFTUc'
ACCESS_TOKEN_API_ENDPOINT = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
REGISTER_URL_API_ENDPOINT = 'https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl'
MPESA_EXPRESS_API_ENDPOINT = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
MPESA_B2C_API_ENDPOINT = 'https://sandbox.safaricom.co.ke/mpesa/b2c/v1/paymentrequest'