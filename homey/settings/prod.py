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
