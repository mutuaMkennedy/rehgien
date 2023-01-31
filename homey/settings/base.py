import os
from datetime import timedelta
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from decouple import config
# import africastalking

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

DEBUG = config('DEBUG', default=False, cast=bool)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

ALLOWED_HOSTS = []

ALLOWED_HOSTS.extend(
    filter(
        None,
        os.environ.get('ALLOWED_HOSTS', '').split(','),
    )
)

ADMINS = [('Mutua', 'do-not-reply@rehgien.com')]
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.humanize',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    # 'allauth.socialaccount.providers.instagram',
    # 'allauth.socialaccount.providers.linkedin',
    # 'allauth.socialaccount.providers.linkedin_oauth2',
    # 'allauth.socialaccount.providers.dropbox',
    # 'allauth.socialaccount.providers.pinterest',
    # map applications
    'leaflet',
    # Homey project applications
    'listings',
    'mortgage',
    'location',
    'contact',
    'profiles',
    'search',
    'chat',
    "partnership",
    "app_accounts",
    "app_notifications",
    "payments",
    "referral",
    # other applications
    'channels',
    'photologue',
    'sortedm2m',
    'crispy_forms',
    'multiselectfield',
    'django_elasticsearch_dsl',
    'rest_framework',
    'rest_framework_gis',
    'rest_framework.authtoken',
    'rest_auth',
    'rest_auth.registration',
    'cloudinary',
    'ckeditor',
    'ckeditor_uploader',
    'corsheaders',
    'django_social_share',
    'markets',
    'rehgien_pro',
    'resource_center',
    'embed_video',
    'formtools',
    'phonenumber_field',
    "django_select2",
    "compressor",
    "django_filters",
    "analytical",
    "django_celery_beat",
    #'haystack',
    # 'tastypie',
    'notifications',
]


ELASTICSEARCH_DSL = {
    'default':{
        'hosts': 'localhost:9200'
    },
}

"""
HAYSTACK_CONNECTIONS = {
    'default': {
            'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
            'URL': 'http://127.0.0.1:9200/',
            'INDEX_NAME': 'haystack',
    },
}
"""
CRISPY_TEMPLATE_PACK = 'uni_form'

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'homey.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),os.path.join(BASE_DIR, 'chat-frontend/build'), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',

)

WSGI_APPLICATION = 'homey.wsgi.application'
ASGI_APPLICATION = "homey.asgi.application"

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "select2": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
}

SELECT2_CACHE_BACKEND = "select2"

CHANNEL_LAYERS = {
    "default":{
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('redis', 6379)],
        },
    },
}

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = '/media/'

LOGIN_REDIRECT_URL = ('homepage')
SIGNUP_REDIRECT_URL = ('homepage')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
    # os.path.join(BASE_DIR, 'chat-frontend/build/static'),
)

STATIC_ROOT = os.path.join(BASE_DIR, '/vol/web/static')
MEDIA_ROOT = os.path.join(BASE_DIR, '/vol/web/media')

# COMPRESS_ENABLED = True

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
    'compressor.finders.CompressorFinder',
)

CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_RESTRICT_BY_USER = True
CKEDITOR_BROWSE_SHOW_DIRS = True
CKEDITOR_ALLOW_NONIMAGE_FILES = False

CKEDITOR_CONFIGS = {
    'blog-post': {
        'skin': 'n1theme',
        'removePlugins':['elementspath', 'iframe'],
        'allowedContent': True,
        # 'skin': 'office2013',
        # 'toolbar_Basic': [
        #     ['Source', '-', 'Bold', 'Italic']
        # ],
        'toolbar_agentprofile': [
            ['Templates'],
            ['Bold',],
            ['Undo', 'Redo'], '/',
            ['Youtube'],
            ['Link', 'Unlink', 'Preview'],
            {'name': 'editing', 'items': ['Find', 'Replace', '-', 'SelectAll']},
            {'name': 'forms',
             'items': ['Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton',
                       'HiddenField']},
            '/',
            {'name': 'paragraph',
             'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-',
                       'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl',
                       'Language']},
            {'name': 'insert','items': ['Image']},
            '/',
            {'name': 'styles', 'items': ['Styles', 'Format', 'Font', 'FontSize']},
            {'name': 'colors', 'items': ['TextColor', 'BGColor']},
            {'name': 'tools', 'items': ['Maximize', 'ShowBlocks']},
            {'name': 'about', 'items': ['About']},
            '/',  # put this to force next toolbar on new line
            {'name': '', 'items': [
                # put the name of your editor.ui.addButton here
                'Bold','Italic','Link','Undo', 'Redo',
                'Templates','Preview','Maximize','Print','Youtube',

            ]},
        ],
        'toolbar': 'agentprofile',  # put selected toolbar config here
        # 'toolbarGroups': [{ 'name': 'document', 'groups': [ 'mode', 'document', 'doctools' ] }],
        # 'height': 291,
        # 'width': '100%',
        # 'filebrowserWindowHeight': 725,
        # 'filebrowserWindowWidth': 940,
        # 'toolbarCanCollapse': True,
        # 'mathJaxLib': '//cdn.mathjax.org/mathjax/2.2-latest/MathJax.js?config=TeX-AMS_HTML',
        'tabSpaces': 4,
        'extraPlugins': ','.join([
            'uploadimage', # the upload image feature
            # your extra plugins here
            'youtube',
            'div',
            'autolink',
            'autoembed',
            'embedsemantic',
            'autogrow',
            # 'devtools',
            'widget',
            'lineutils',
            'clipboard',
            'dialog',
            'dialogui',
            'elementspath'
        ]),
    },
}

LEAFLET_CONFIG = {
    'SPATIAL_EXTENT': (33.8679, -4.816276, 41.97685, 4.629931),
    # 'TILES': 'mapbox://styles/reykennedy/cjr359eyw0t9n2rrzr4fbv8uy',
    'DEFAULT_CENTER': (-1.10, 37.01),
    'DEFAULT_ZOOM': 10,
    'MAX_ZOOM':20,
    'MIN_ZOOM':3,
    'SCALE': 'both',
    'ATTRIBUTION_PREFIX': 'Rehgien',
    'RESET_VIEW': False,
    'DRAW':False,
    'FORCE_IMAGE_PATH': True,
    'NO_GLOBALS':False,
    'PLUGINS': {
        'forms': {
                # 'js': 'https://unpkg.com/leaflet-geosearch@3.0.0/dist/geosearch.umd.js',
                # 'css': 'https://unpkg.com/leaflet-geosearch@3.0.0/dist/geosearch.css',
                'auto-include': True
        },
    }

}


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework.authentication.TokenAuthentication',
    )
}

# REST_USE_JWT = True

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=6),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    # 'ROTATE_REFRESH_TOKENS': False,
    # 'BLACKLIST_AFTER_ROTATION': True,
    # 'UPDATE_LAST_LOGIN': False,
    #
    # 'ALGORITHM': 'HS256',
    # 'SIGNING_KEY': settings.SECRET_KEY,
    # 'VERIFYING_KEY': None,
    # 'AUDIENCE': None,
    # 'ISSUER': None,
    #
    # 'AUTH_HEADER_TYPES': ('Bearer',),
    # 'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    # 'USER_ID_FIELD': 'id',
    # 'USER_ID_CLAIM': 'user_id',
    #
    # 'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    # 'TOKEN_TYPE_CLAIM': 'token_type',
    #
    # 'JTI_CLAIM': 'jti',
    #
    # 'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    # 'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    # 'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

REST_AUTH_SERIALIZERS = {
    'TOKEN_SERIALIZER': 'chat.apis.serializers.StreamTokenSerializer',
}

REST_AUTH_REGISTER_SERIALIZERS = {
    'REGISTER_SERIALIZER': 'profiles.apis.serializers.CustomRegisterSerializer',
}

AUTH_USER_MODEL = 'profiles.User'

CORS_ORIGIN_WHITELIST = [
    'http://localhost:3000',
    'http://127.0.0.1:8000',
    'http://165.227.185.180'
]
# CORS_ORIGIN_ALLOW_ALL = True

# allauth further Configs
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_SIGNUP_FORM_CLASS = 'profiles.forms.profile_form'


TWILIO_ACCOUNT_SID = 'ACf67d31ba29c20feff49cadc08fad69f1'
TWILIO_AUTH_TOKEN = '6041ece7b205b55d92d0415ccbe424bb'
TWILIO_API_KEY = 'SKa49ccc790e56921af3eab4a615491c91'
TWILIO_API_SECRET = 'oML64f6ovDPuTOkOGQ6bP77yqyNPyw33'

# CELERY STUFF
BROKER_URL =  'redis://redis:6379'
CELERY_RESULT_BACKEND = 'redis://redis:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
CELERY_ENABLE_UTC = True
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers.DatabaseScheduler'

# This setting is not needed as celery beate allows us to schedule tasks from the admin panel
# from celery.schedules import crontab
# CELERY_BEAT_SCHEDULE = {
#       'send_progress_everyday': {
#         'task': 'send_pro_profile_completion_progress_message',
#         'schedule': crontab()
#       }
# }

DJANGO_NOTIFICATIONS_CONFIG = { 'USE_JSONFIELD': True}

SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'METHOD': 'oauth2',
        # 'SDK_URL': '//connect.facebook.net/{locale}/sdk.js',
        'SCOPE': ['email', 'public_profile'],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'INIT_PARAMS': {'cookie': True},
        'FIELDS': [
            'id',
            'first_name',
            'last_name',
            'middle_name',
            'name',
            'name_format',
            'picture',
            'short_name'
        ],
        'EXCHANGE_TOKEN': True,
        # 'LOCALE_FUNC': 'path.to.callable',
        'VERIFIED_EMAIL': False,
        'VERSION': 'v7.0',
    },
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

# Analytic services
CLICKY_SITE_ID = config('CLICKY_SITE_ID')
GOOGLE_ANALYTICS_GTAG_PROPERTY_ID = config('GOOGLE_ANALYTICS_GTAG_PROPERTY_ID')
HOTJAR_SITE_ID = config('HOTJAR_SITE_ID')
