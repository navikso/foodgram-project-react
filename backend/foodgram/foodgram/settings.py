import os

# from datetime import timedelta
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()


BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = (
    'django-insecure-#3x3o=o#8r3o!x-7=2&&m$hgc*!vwh^j-hi__nxas1blytru7^'
)
# SECRET_KEY = 'm%(5u7nv9j2%@3xb%#c3p-$9&0$kq$j6l@9+@ogairu48a+dy+'

DEBUG = True

ALLOWED_HOSTS = ['*']

AUTH_USER_MODEL = 'users.UserProfile'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djoser',

    'rest_framework',
    # 'rest_framework_simplejwt',

    'api.apps.ApiConfig',
    'authentication.apps.AuthenticationConfig',
    'recipes.apps.RecipesConfig',
    'users.apps.UsersConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'foodgram.urls'

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

WSGI_APPLICATION = 'foodgram.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.postgresql'),
        'NAME': os.getenv('DB_NAME', default='postgres'),
        'USER': os.getenv('POSTGRES_USER', default='postgres'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', default='postgres'),
        'HOST': os.getenv('DB_HOST', default='localhost'),
        'PORT': os.getenv('DB_PORT', default=5432)
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'UserAttributeSimilarityValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.'
            'password_validation.MinimumLengthValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.'
            'password_validation.CommonPasswordValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.'
            'password_validation.NumericPasswordValidator'
        ),
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

CSV_FILES_DIR = os.path.join(BASE_DIR, 'static/docs')


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.'
                                'LimitOffsetPagination',
    'PAGE_SIZE': 10,

    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],

    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
}

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'sent_emails')
EMAIL_SUBJECT = 'Код подтверждения'
EMAIL_SENDER = 'from@example.com'

DJOSER = {
    'LOGIN_FIELD': 'email',
    'SERIALIZERS': {
        'user_create': 'authentication.serializers.CreateUserSerializer',
        'user': 'api.serializers.UserSerializer',
        'current_user': 'api.serializers.UserSerializer',
    },
    'PERMISSIONS': {
        'user': 'djoser.permissions.CurrentUserOrAdminOrReadOnly',
        'user_list': 'rest_framework.permissions.AllowAny',
        # 'user_delete': 'rest_framework.permissions.IsAdminUser',
        # 'token_create': 'rest_framework.permissions.AllowAny',
    }
}

# SIMPLE_JWT = {
#     'AUTH_TOKEN_CLASSES': (
#         'rest_framework_simplejwt.tokens.AccessToken',
#     ),
#     'ACCESS_TOKEN_LIFETIME': timedelta(days=7),
# }


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
}
