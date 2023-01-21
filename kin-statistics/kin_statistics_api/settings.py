import os
import datetime
from pathlib import Path

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = bool(int(os.environ.get('DEBUG')))
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
NOSE_ARGS = ['--nocapture', '--nologcapture']

ALLOWED_HOSTS = ['*']

CORS_ALLOW_ALL_ORIGINS = True  # If this is used then `CORS_ALLOWED_ORIGINS` will not have any effect
CORS_ALLOW_CREDENTIALS = True

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'drf_yasg',
    'corsheaders',

    'api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DATABASE_NAME'),
        'USER': os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        'HOST': os.getenv('DATABASE_HOST', 'localhost'),
        'PORT': os.getenv('DATABASE_PORT', '5432')
    }
}
MIGRATION_MODULES = {'api': 'api.infrastructure.migrations'}

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = '/media'

LOCAL_TIMEZONE = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

TOKEN_LIFE_MINUTES = int(os.environ.get('TOKEN_LIFE_MINUTES'))

# Telegram
TELEGRAM_API_ID = int(os.getenv('TELEGRAM_API_ID'))
TELEGRAM_API_HASH = os.getenv('TELEGRAM_API_HASH')
TELEGRAM_SESSION_STRING = os.getenv('TELEGRAM_SESSION_STRING')

MONGO_DB_CONNECTION_STRING = os.getenv('MONGO_DB_CONNECTION_STRING')

MAX_SUBSCRIPTIONS_ALLOWED = os.getenv('MAX_SUBSCRIPTIONS_ALLOWED', 12)

KIN_TOKEN = os.getenv('KIN_TOKEN')

USER_REPORTS_FOLDER_PATH = os.getenv("USER_REPORTS_FOLDER_PATH")


# Celery
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND')
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'


# ML models
SKLEARN_VECTORIZER_PATH = BASE_DIR / os.getenv('SKLEARN_VECTORIZER_PATH')
KERAS_TOKENIZER_PATH = BASE_DIR / os.getenv('KERAS_TOKENIZER_PATH')
KNN_MODEL_PATH = BASE_DIR / os.getenv('KNN_MODEL_PATH')
SVC_MODEL_PATH = BASE_DIR / os.getenv('SVC_MODEL_PATH')
GAUSSIAN_MODEL_PATH = BASE_DIR / os.getenv('GAUSSIAN_MODEL_PATH')
LSTM_MODEL_PATH = BASE_DIR / os.getenv('LSTM_MODEL_PATH')


# Sentiment
SENTIMENT_DICTIONARY_PATH = BASE_DIR / os.getenv('SENTIMENT_DICTIONARY_PATH')
STOP_WORDS_PATH = BASE_DIR / os.getenv('STOP_WORDS_PATH')

# Reports generation
MAX_SYNCHRONOUS_REPORTS_GENERATION = int(os.getenv("MAX_SYNCHRONOUS_REPORTS_GENERATION", 3))
