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

EMAIL_USE_TLS = True
EMAIL_HOST = "smtp.eu.mailgun.org"
EMAIL_HOST_USER = "postmaster@mg.rehgien.com"
EMAIL_HOST_PASSWORD = '6b096ae5c848dcdd0d227aab48294bd3-6ae2ecad-a5b2b2ce'
EMAIL_PORT = 587
EMAIL_USE_SSL = False
DEFAULT_FROM_EMAIL = 'Rehgien <do-not-reply@rehgien.com>'

#claudinary settings
cloudinary.config(
  cloud_name = "rehgien-inc",
  api_key = "435726737312679",
  api_secret = "0ULgyGJ9Mj77dbIO5vrbrfB_NFY"
)

# Twilio settings
TWILIO_CONVERSATIONS_SERVICE_SID = 'IS784d626c2f504a57a39d7a8acc076d24'
TWILIO_MESSAGING_SERVICE_SID = 'MGfe6adc69206ff2aede13c3e540aefd0d'
TWILIO_PHONE_NUMBER = '+18456226952'

# Sentry configuration
sentry_sdk.init(
    dsn="https://a1ebe35872d54deaa1b75ea6b631f3e4@o544386.ingest.sentry.io/5665554",
    integrations=[DjangoIntegration()],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production,
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)

# M-pesa daraja settings
CONSUMER_KEY = "EiXmkNt4ha8TEFbGvmMuC7cm6mGRhR8p"
CONSUMER_SECRET = 'zaxeviE8GB7GFTUc'
ACCESS_TOKEN_API_ENDPOINT = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
REGISTER_URL_API_ENDPOINT = 'https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl'
MPESA_EXPRESS_API_ENDPOINT = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
MPESA_B2C_API_ENDPOINT = 'https://sandbox.safaricom.co.ke/mpesa/b2c/v1/paymentrequest'