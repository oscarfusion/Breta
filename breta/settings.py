"""
Django settings for breta project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys
import dj_database_url
TESTING = len(sys.argv) > 1 and sys.argv[1] == 'test'
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', '$$b*2%yetxq**-*)^70v31ml!^p@#$d(s=hyb4jbdg^u*^p^(3')


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['easy.breta.com']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'cities_light',
    'rest_framework',
    'rest_framework.authtoken',
    'django_jenkins',
    'pipeline',
    'widget_tweaks',
    'corsheaders',
    'constance',
    'constance.backends.database',
    'tinymce',

    'accounts',
    'activities',
    'core',
    'breta_messages',
    'projects',
    'payments',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    # 'pipeline.middleware.MinifyHTMLMiddleware',
)

ROOT_URLCONF = 'breta.urls'

WSGI_APPLICATION = 'breta.wsgi.application'

# STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "breta/static"),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'pipeline.finders.PipelineFinder',
)

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(),
}

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'breta/templates'),
)

STATIC_ROOT = 'staticfiles'
MEDIA_ROOT = 'mediafiles'

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

AUTH_USER_MODEL = 'accounts.User'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.DjangoModelPermissions',
    ),
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',),
    'PAGINATE_BY': 100,
    'PAGINATE_BY_PARAM': 'page_size',
    'MAX_PAGINATE_BY': 100,
    'DEFAULT_PAGINATION_SERIALIZER_CLASS':
        'rest_framework_ember.pagination.PaginationSerializer',
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework_ember.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser'
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework_ember.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework.authentication.TokenAuthentication',
        'core.authentication.BretaAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',  # optional
    ),
}

JENKINS_TASKS = (
    'django_jenkins.tasks.run_pep8',
    'django_jenkins.tasks.run_pyflakes',
)

CORS_ORIGIN_WHITELIST = (
    'localhost:4200',
    'easy.breta.com:4200'
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')
STRIPE_PUBLIC_KEY = os.environ.get('STRIPE_PUBLIC_KEY')

MAILCHIMP_API_KEY = os.environ.get('MAILCHIMP_API_KEY')
MAILCHIMP_DEFAULT_LIST = os.environ.get('MAILCHIMP_DEFAULT_LIST')

from static_settings import *  # noqa

DEFAULT_FROM_EMAIL = 'Breta team <support@breta.com>'
ADMINS = ['elliot@breta.com']
CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'

CONSTANCE_CONFIG = {
    'BRETA_FEE': (10, 'Percent of price users pays as remuneration for using Breta'),
    'PO_FEE': (30, 'Percent of price project owner\'s pays as remuneration for using BRETA'),
    'DEVELOPER_FEE': (10, 'Percent of price project owner\'s pays as remuneration for using BRETA'),
    'DISABLE_PAYOUTS': (False, 'Disable payouts and withdraws'),
    'REFERRAL_TAX_PERCENT': (1, 'Percent, which every user pays for their referrers if their exist')
}

DOMAIN = 'https://easy.breta.com'
API_DOMAIN = 'https://easy.breta.com/app'

BROKER_URL = 'redis://localhost:6379/0'

from datetime import timedelta  # noqa

CELERYBEAT_SCHEDULE = {
    'test-task-beat': {
        'task': 'core.tasks.debug_task',
        'schedule': timedelta(seconds=60),
    },
    'milestones-due-today': {
        'task': 'projects.tasks.milestones_due_today',
        'schedule': timedelta(days=1),
    }
}

CELERY_TIMEZONE = 'UTC'

try:
    from local_settings import *  # noqa
except ImportError:
    pass

if DEBUG:
    INSTALLED_APPS += ('debug_toolbar.apps.DebugToolbarConfig',)
    MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
