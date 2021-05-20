from homey.settings.base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

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
