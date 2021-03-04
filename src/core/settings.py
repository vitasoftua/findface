"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""
import datetime
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-nag20dfzvgkx-7y^bleur-r%!5@5bh(ev$czx-ssw*@ph5k_7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.environ.get('WEB_HOSTNAME', '').split(',')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'bootstrap4',
    'corsheaders',
    'channels',
    'drf_yasg',
    'fcm_django',
    'rest_framework',
    'rest_framework_jwt',

    'accounts',
    'core',
    'faces',

    'django_cleanup',  # should go after your apps
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.environ.get('POSTGRES_HOST'),
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Kiev'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

from django.utils.translation import gettext_lazy as _
LANGUAGES = (
    ('ru', _('Russian')),
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, '..', 'public')
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'), )

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, '..', 'media')


AUTH_USER_MODEL = 'accounts.User'
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login'
LOGOUT_REDIRECT_URL = '/'


REDIS_HOST = os.environ.get('REDIS_HOST')

# rest_framework
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',

    'DATE_FORMAT': '%d.%m.%y',
    'DATETIME_FORMAT': '%d.%m.%y %H:%M:%S',
    'DATE_INPUT_FORMATS': ['%d.%m.%y'],
    'DATETIME_INPUT_FORMATS': ['%d.%m.%y %H:%M:%S'],
}


# rest_framework_jwt
JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=3),
    'JWT_RESPONSE_PAYLOAD_HANDLER':
        'accounts.utils.jwt_response_payload_handler',
}


# drf_yasg
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'basic': {
            'type': 'basic'
        }
    },
    'DEFAULT_INFO': 'core.swagger.api_info',
}


# celery
CELERY_BROKER_URL = 'amqp://{}'.format(os.environ.get('RABBITMQ_HOST'))


# Channels
ASGI_APPLICATION = 'faces.routing.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [(REDIS_HOST, 6379)],
        },
    },
}
ROOM_NAME_NOTIFICATIONS = 'chat_notifications'
ROOM_NAME_FACES = 'chat_faces'


# fcm_django
FCM_DJANGO_SETTINGS = {
    # "APP_VERBOSE_NAME": "[string for AppConfig's verbose_name]",
    "FCM_SERVER_KEY": os.environ.get('FCM_SERVER_KEY'),
    "ONE_DEVICE_PER_USER": False,
    "DELETE_INACTIVE_DEVICES": True,
    "USER_MODEL": 'accounts.User'
}


FFS_API_URL = os.environ.get('FFS_API_URL')
FFS_API_TOKEN = os.environ.get('FFS_API_TOKEN')
FFS_UPLOAD_URL = os.environ.get('FFS_UPLOAD_URL')

if DEBUG:
    ALLOWED_HOSTS = ['*']
    CORS_ORIGIN_ALLOW_ALL = True


import logging.config
LOGGING_CONFIG = None
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            # exact format is not important, this is the minimum information
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        },
    },
})
