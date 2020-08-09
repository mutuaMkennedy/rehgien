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
    'chat',
    # other applications
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
    'django_social_share'
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
    os.path.join(BASE_DIR, 'chat-frontend/build/static'),
)

STATIC_ROOT = os.path.join(BASE_DIR, 'assets_new')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_RESTRICT_BY_USER = True
CKEDITOR_BROWSE_SHOW_DIRS = True
CKEDITOR_ALLOW_NONIMAGE_FILES = False

CKEDITOR_CONFIGS = {
    'agent_profile': {
        'skin': 'n1theme',
        'removePlugins':'elementspath',
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
            # {'name': 'editing', 'items': ['Find', 'Replace', '-', 'SelectAll']},
            # {'name': 'forms',
            #  'items': ['Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton',
            #            'HiddenField']},
            # '/',
            # {'name': 'paragraph',
            #  'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-',
            #            'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl',
            #            'Language']},
            # {'name': 'insert','items': ['Image']},
            # '/',
            # {'name': 'styles', 'items': ['Styles', 'Format', 'Font', 'FontSize']},
            # {'name': 'colors', 'items': ['TextColor', 'BGColor']},
            # {'name': 'tools', 'items': ['Maximize', 'ShowBlocks']},
            # {'name': 'about', 'items': ['About']},
            # '/',  # put this to force next toolbar on new line
            # {'name': '', 'items': [
            #     # put the name of your editor.ui.addButton here
            #     'Bold','Italic','Link','Undo', 'Redo',
            #     'Templates','Preview','Maximize','Print','Youtube',
            #
            # ]},
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

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        # 'rest_framework.authentication.TokenAuthentication',
    )
}

REST_AUTH_SERIALIZERS = {
    'TOKEN_SERIALIZER': 'chat.apis.serializers.StreamTokenSerializer',
}

AUTH_USER_MODEL = 'profiles.User'

CORS_ORIGIN_WHITELIST = [
    'http://localhost:3000',
    'http://127.0.0.1:8000',
    'http://165.227.185.180'
]
# CORS_ORIGIN_ALLOW_ALL = True

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

TWILIO_ACCOUNT_SID = 'AC1db0e8cfbae1e3b9b5834772c0ef8d6c'
TWILIO_API_KEY = 'SK5c969e58ab96a19249489add62911305'
TWILIO_API_SECRET = 'qDSWimtxgzelWceywCF2Sbcslr7s1o7P'
TWILIO_CHAT_SERVICE_SID = 'ISe0ef1fd1e4f444aba9ccc09b28047ab5'
TWILIO_AUTH_TOKEN = '7f70419841a1632045d657089acd65c1'

STREAM_API_KEY = 'ke9puq24fsgq'
STREAM_API_SECRET = '8efsewntkc7mpzvevw245b768w5pddxqc5muk8u2gqxpeggdymygmts4r6xh7zuh'
