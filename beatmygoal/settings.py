"""
Django settings for beatmygoal project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys
import dj_database_url
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), '../templates')
)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'd5(+491*&)&l)%7e9o167l=@i5)42vt2qy%xpoy+n@*p&tlx49'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

#ALLOWED_HOSTS = []

ADMINS = (('beatmygoal', 'beatmygoal@googlegroups.com'))

# Application definition
if 'ON_HEROKU' in os.environ:
    AWS_STORAGE_BUCKET_NAME = 'beatmygoalfiles'
    STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
    S3_URL = 'http://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
    STATIC_URL = S3_URL
    AWS_S3_SECURE_URLS = False       # use http instead of https
    AWS_QUERYSTRING_AUTH = False     # don't add complex authentication-related query parameters for requests
    AWS_S3_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY', '')      # enter your access key id
    AWS_S3_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_KEY', '')
    STATIC_URL = 'http://' + AWS_STORAGE_BUCKET_NAME + '.s3.amazonaws.com/'
    ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'
    MEDIA_URL = S3_URL
    STATIC_URL = '/static/'
    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, "static"),
    )
else:
    STATIC_URL = '/static/'
    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, "static"),
    )
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    MEDIA_URL = '/media/'



INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'south',
    'django_nose',
    'storages',
    'djoauth2',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'beatmygoal.middleware.AutoLogout',
)


#venmo
DJOAUTH2_SSL_ONLY = False






ROOT_URLCONF = 'beatmygoal.urls'

WSGI_APPLICATION = 'beatmygoal.wsgi.application'



#Handle session is not Json Serializable
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

# Auto logout delay in minutes
AUTO_LOGOUT_DELAY = 100 #equivalent to 1 minutes

# Close the session when user closes the browser
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Los_Angeles'

USE_I18N = True

USE_L10N = True

USE_TZ = False  # changed to use datetime package


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/


# Parse database configuration from $DATABASE_URL
import os
if 'ON_HEROKU' in os.environ:
    DATABASES['default'] =  dj_database_url.config()
    DEBUG = False

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

try:
    from local_settings import *
except Exception as e:
    pass


# Static asset configuration
# import os
# PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))



# STATIC_ROOT = 'staticfiles'



# STATIC_URL = '/static/'


# STATICFILES_DIRS = (
#     os.path.join(PROJECT_PATH, '../static'),
# )



AUTH_USER_MODEL = 'core.BeatMyGoalUser'


TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'


EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'beatmygoalcal@gmail.com'
EMAIL_HOST_PASSWORD = 'beatmygoal123'
EMAIL_PORT = 587



import logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
        }
    }
}
