"""
Django settings for NoInventoryProject project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from pymongo import *
import logging
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'va02(io6a3jzc3w5!f$&hdd%j1$%-%atazd-m7em$m3j1vx5b6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']


##Configuracion y conexion del cliente para MongoDB
MONGO_HOST='localhost'
MONGO_PORT=27017
ON_COMPOSE = os.environ.get('COMPOSE')
ON_HEROKU = os.environ.get('HEROKU')
if ON_HEROKU:
	CLIENTE=MongoClient('mongodb://hugo:hugo@ds011923.mlab.com:11923/noinventory')
elif ON_COMPOSE:
	CLIENTE=MongoClient('mongodb://hugo:hugo@ds011923.mlab.com:11923/noinventory')
else:
	CLIENTE= MongoClient(host=MONGO_HOST,port=MONGO_PORT)

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'NoInventory',
    'bootstrapform',
    'easy_maps',
)


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

AUTH_PROFILE_MODULE = "NoInventory.UserProfile"


ROOT_URLCONF = 'NoInventoryProject.urls'

WSGI_APPLICATION = 'NoInventoryProject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/


if DEBUG == True:
    STATIC_URL = '/static/'
    STATIC_PATH = os.path.join(BASE_DIR,'static')
    STATIC_ROOT = 'staticfiles'
    STATICFILES_DIRS = (
    STATIC_PATH,
    )
else:
    STATIC_URL = '/var/www/static/'
    STATIC_ROOT = 'staticfiles'





MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')



TEMPLATE_PATH = os.path.join(BASE_DIR, 'templates')
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_PATH],
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
