import os

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(PROJECT_DIR)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

TIME_ZONE = 'Europe/Amsterdam'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True

MEDIA_ROOT = ''
MEDIA_URL = ''
STATIC_ROOT = '/srv/www/tickettracker/htdocs/static/'
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/static/admin/'

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/o/'

STATICFILES_DIRS = (
    os.path.join(PROJECT_DIR, 'static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

FIXTURE_DIRS = (os.path.join(PROJECT_DIR, 'fixtures'),)

SECRET_KEY = '00%qv)ek(b*i$=yiv96&)2gd0e$*$h=yv21r-g2=ou6xj0jjk&'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

AUTH_PROFILE_MODULE = 'userprofile.UserProfile'

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'management.urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',

    # custom authentication app which adds a userprofile when a user is created
    'management.apps.userprofile',

    # Ticket application
    'management.apps.ticket',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

TEST_RUNNER = 'management.CoverageRunner'
COVERAGE_MODULES = (
    'management.apps.ticket.models',
)

from site_settings import *
