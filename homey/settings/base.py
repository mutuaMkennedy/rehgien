import os
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ib)4kavk+9ds#_!v8y5*qoy2@)g1gfa@y2u(4tpvej$feb!!oj'

ALLOWED_HOSTS = ['localhost','165.227.185.180','127.0.0.1']


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
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # 'allauth.socialaccount.providers.facebook',
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
    # other applications
    'photologue',
    'sortedm2m',
    'crispy_forms',
    'multiselectfield',
    'django_elasticsearch_dsl',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',
    'rest_auth.registration',
    'cloudinary',
    #'haystack',
    # 'tastypie',
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
]

ROOT_URLCONF = 'homey.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

LOGIN_REDIRECT_URL = ('listings:homepage')
SIGNUP_REDIRECT_URL = ('listing:homepage')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATIC_ROOT = os.path.join(BASE_DIR, 'assets_new')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

LEAFLET_CONFIG = {
    'DEFAULT_CENTER': (-1.10, 37.01),
    'DEFAULT_ZOOM': 10,
    'MAX_ZOOM':20,
    'MIN_ZOOM':3,
    'SCALE': 'both',
    'ATTRIBUTION_PREFIX': 'Powered by leaflet, inspired by Rehgien',


}

#claudinary settings
cloudinary.config(
  cloud_name = "rehgien",
  api_key = "113141524396467",
  api_secret = "BAsPMg7zobSDbjzPs0yrwnCf-S0"
)

# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#         'rest_framework_simplejwt.authentication.JWTAuthentication',
#     )
# }

# allauth further Configs
ACCOUNT_AUTHENTICATION_METHOD = "username"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_SIGNUP_FORM_CLASS = 'profiles.forms.profile_form'

EMAIL_USE_TLS = True
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = "mutuakennedy81@gmail.com"
EMAIL_HOST_PASSWORD = 'ierhjgdkfdmrghml'
EMAIL_PORT = 587
EMAIL_USE_SSL = False
