## Django settings for ASKBOT enabled project.
import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), 'third_party'))
import logging
import askbot

#this line is added so that we can import pre-packaged askbot dependencies
sys.path.append(os.path.join(os.path.dirname(askbot.__file__), 'deps'))

DEBUG = True 
TEMPLATE_DEBUG = False #keep false when debugging jinja2 templates
INTERNAL_IPS = ('127.0.0.1',)

ADMINS = (
    ('ADMIN', 'EMAIL'),
)

MANAGERS = ADMINS
if (os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine') or
    os.getenv('SETTINGS_MODE') == 'prod'):
    # Running on production App Engine, so use a Google Cloud SQL database.
    DATABASES = {
      'default': {
      'ENGINE': 'google.appengine.ext.django.backends.rdbms',
      'INSTANCE': 'INSTANCE',
      'NAME': 'NAME',
      }
    }
    RECAPTCHA_PRIVATE_KEY = "KEY"
    RECAPTCHA_PUBLIC_KEY = "KEY"
else:
  DATABASE_ENGINE = 'mysql' # only postgres (>8.3) and mysql are supported so far others have not been tested yet
  DATABASE_NAME = 'django'             # Or path to database file if using sqlite3.
  DATABASE_USER = 'bf'             # Not used with sqlite3.
  DATABASE_PASSWORD = 'pass'         # Not used with sqlite3.
  DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
  DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.
  RECAPTCHA_PRIVATE_KEY = "KEY"
  RECAPTCHA_PUBLIC_KEY = "KEY"

#outgoing mail server settings
SERVER_EMAIL = ''
DEFAULT_FROM_EMAIL = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_SUBJECT_PREFIX = ''
EMAIL_HOST=''
EMAIL_PORT=''
EMAIL_USE_TLS=False
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

#incoming mail settings
#after filling out these settings - please
#go to the site's live settings and enable the feature
#"Email settings" -> "allow asking by email"
#
#   WARNING: command post_emailed_questions DELETES all 
#            emails from the mailbox each time
#            do not use your personal mail box here!!!
#
IMAP_HOST = ''
IMAP_HOST_USER = ''
IMAP_HOST_PASSWORD = ''
IMAP_PORT = ''
IMAP_USE_TLS = False

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Moscow'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True
LANGUAGE_CODE = 'en'

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'askbot', 'upfiles')
MEDIA_URL = '/upfiles/'

PROJECT_ROOT = os.path.dirname(__file__)

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin/media/'

# Make up some unique string, and don't share it with anybody.
SECRET_KEY = 'THINK OF ONE YOURSELF' 

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
    #below is askbot stuff for this tuple
    'askbot.skins.loaders.filesystem_load_template_source',
    #'django.template.loaders.eggs.load_template_source',
)


MIDDLEWARE_CLASSES = (
    #'django.middleware.gzip.GZipMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.cache.FetchFromCacheMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    #'django.middleware.sqlprint.SqlPrintingMiddleware',

    #below is askbot stuff for this tuple
    'askbot.middleware.anon_user.ConnectToSessionMessagesMiddleware',
    'askbot.middleware.forum_mode.ForumModeMiddleware',
    'askbot.middleware.pagesize.QuestionsPageSizeMiddleware',
    'askbot.middleware.cancel.CancelActionMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
    'askbot.middleware.view_log.ViewLogMiddleware',
    'askbot.middleware.spaceless.SpacelessMiddleware',
)


ROOT_URLCONF =  'urls'


#UPLOAD SETTINGS
FILE_UPLOAD_TEMP_DIR = os.path.join(
                                os.path.dirname(__file__), 
                                'tmp'
                            ).replace('\\','/')

FILE_UPLOAD_HANDLERS = (
    'django.core.files.uploadhandler.MemoryFileUploadHandler',
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
)
ASKBOT_ALLOWED_UPLOAD_FILE_TYPES = ('.jpg', '.jpeg', '.gif', '.bmp', '.png', '.tiff')
ASKBOT_MAX_UPLOAD_FILE_SIZE = 1024 * 1024 #result in bytes
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'


TEMPLATE_DIRS = ('templates',) #template have no effect in askbot, use the variable below
#TEMPLATE_DIRS = (,) #template have no effect in askbot, use the variable below
#ASKBOT_EXTRA_SKINS_DIR = #path to your private skin collection
#take a look here http://askbot.org/en/question/207/

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'askbot.context.application_settings',
    #'django.core.context_processors.i18n',
    'askbot.user_messages.context_processors.user_messages',#must be before auth
    'django.core.context_processors.auth', #this is required for admin
    'django.core.context_processors.csrf', #necessary for csrf protection
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect'
)


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',

    #all of these are needed for the askbot
    'django.contrib.admin',
    'django.contrib.humanize',
    'django.contrib.sitemaps',
    #'debug_toolbar',
    'askbot',
    'askbot.deps.django_authopenid',
    #'askbot.importers.stackexchange', #se loader
    # 'south', TODO(kazeevn) investigate how to use with CloudSQL
    'askbot.deps.livesettings',
    'keyedcache',
    'robots',
    'django_countries',
    'djcelery',
    'djkombu',
    'followit',
    #'avatar',#experimental use git clone git://github.com/ericflo/django-avatar.git$
    'notes',
    'captcha',
    'social.apps.django_app.default'
)


#setup memcached for production use!
#see http://docs.djangoproject.com/en/1.1/topics/cache/ for details
CACHES = {
    'default': {
    'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
    'TIMEOUT': 6000,
    }
}
CACHE_TIMEOUT=6000
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
#CACHE_BACKEND = 'memcached://'
#needed for django-keyedcache
CACHE_PREFIX = 'askbot' #make this unique
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'askbot.deps.django_authopenid.backends.AuthBackend',
    'social.backends.open_id.OpenIdAuth',
    'social.backends.google.GoogleOpenId',
    'social.backends.google.GoogleOAuth2',
    'social.backends.google.GoogleOAuth',
    'social.backends.twitter.TwitterOAuth',
    'social.backends.yahoo.YahooOpenId',
)

#logging settings
LOG_FILENAME = 'askbot.log'
logging.basicConfig(
    filename=os.path.join(os.path.dirname(__file__), 'log', LOG_FILENAME),
    level=logging.CRITICAL,
    format='%(pathname)s TIME: %(asctime)s MSG: %(filename)s:%(funcName)s:%(lineno)d %(message)s',
)

###########################
#
#   this will allow running your forum with url like http://site.com/forum
#
#   ASKBOT_URL = 'forum/'
#
ASKBOT_URL = 'qa/' #no leading slash, default = '' empty string
ASKBOT_TRANSLATE_URL = True #translate specific URLs
_ = lambda v:v #fake translation function for the login url
LOGIN_URL = '/social/login/google'
LOGIN_REDIRECT_URL = '/assets/close.html'
#note - it is important that upload dir url is NOT translated!!!
#also, this url must not have the leading slash
ALLOW_UNICODE_SLUGS = False
ASKBOT_USE_STACKEXCHANGE_URLS = False #mimic url scheme of stackexchange

#Celery Settings
BROKER_TRANSPORT = "djkombu.transport.DatabaseTransport"
CELERY_ALWAYS_EAGER = True

import djcelery
djcelery.setup_loader()

if (os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine') or
    os.getenv('SETTINGS_MODE') == 'prod'):
    DOMAIN_NAME='brain-of.appspot.com'
else:
    DOMAIN_NAME = 'localhost'

CSRF_COOKIE_NAME = 'PHPSSID' # (kazeevn) Security throught obscurity is our way!
CSRF_COOKIE_DOMAIN = DOMAIN_NAME
