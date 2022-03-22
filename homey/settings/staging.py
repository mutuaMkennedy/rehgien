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

# M-pesa daraja settings
CONSUMER_KEY = "EiXmkNt4ha8TEFbGvmMuC7cm6mGRhR8p"
CONSUMER_SECRET = 'zaxeviE8GB7GFTUc'
ACCESS_TOKEN_API_ENDPOINT = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
REGISTER_URL_API_ENDPOINT = 'https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl'
MPESA_EXPRESS_API_ENDPOINT = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
MPESA_B2C_API_ENDPOINT = 'https://sandbox.safaricom.co.ke/mpesa/b2c/v1/paymentrequest'