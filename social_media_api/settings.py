"""
Django settings for social_media_api project.
Production-ready configuration for Heroku deployment.
"""

from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv

load_dotenv()

# ------------------------------------------------------------------------------
# BASE DIRECTORY
# ------------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ------------------------------------------------------------------------------
# SECURITY & DEBUG
# ------------------------------------------------------------------------------
SECRET_KEY = os.getenv("SECRET_KEY")

# NEVER use DEBUG=True in production
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")
DEBUG = False

# Correct ALLOWED_HOSTS syntax
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost").split(",")
# HEROKU_APP = os.getenv("HEROKU_APP_NAME")

# if HEROKU_APP:
#     ALLOWED_HOSTS.append(f"{HEROKU_APP}.herokuapp.com")

# ALLOWED_HOSTS.append("*")  # Allow all hosts temporarily for Heroku routing

# ------------------------------------------------------------------------------
# APPLICATIONS
# ------------------------------------------------------------------------------
INSTALLED_APPS = [
    # Django core
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    "whitenoise.runserver_nostatic",
    'django.contrib.staticfiles',

    # Third-party
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',

    # Custom apps
    'accounts',
    'posts',
    'notifications',
]

# ------------------------------------------------------------------------------
# MIDDLEWARE
# ------------------------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ------------------------------------------------------------------------------
# URLS / WSGI
# ------------------------------------------------------------------------------
ROOT_URLCONF = 'social_media_api.urls'
WSGI_APPLICATION = 'social_media_api.wsgi.application'

# ------------------------------------------------------------------------------
# TEMPLATES
# ------------------------------------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ------------------------------------------------------------------------------
# DATABASE (Local Dev + Heroku)
# ------------------------------------------------------------------------------
if os.getenv("DATABASE_URL"):
    # Heroku PostgreSQL
    DATABASES = {
        "default": dj_database_url.config(
            default=os.getenv("DATABASE_URL"),
            conn_max_age=600,
            ssl_require=True
        )
    }
# else:
#     # Local PostgreSQL
#     DATABASES = {
#         "default": {
#             "ENGINE": "django.db.backends.postgresql",
#             "NAME": os.getenv("DB_NAME"),
#             "USER": os.getenv("DB_USER"),
#             "PASSWORD": os.getenv("DB_PASSWORD"),
#             "HOST": os.getenv("DB_HOST", "localhost"),
#             "PORT": os.getenv("DB_PORT", "5432"),
#         }
#     }

# ------------------------------------------------------------------------------
# REST FRAMEWORK
# ------------------------------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
}

AUTH_USER_MODEL = 'accounts.User'

# ------------------------------------------------------------------------------
# PASSWORD VALIDATION
# ------------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ------------------------------------------------------------------------------
# INTERNATIONALIZATION
# ------------------------------------------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ------------------------------------------------------------------------------
# STATIC / MEDIA
# ------------------------------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ------------------------------------------------------------------------------
# SECURITY: Production Best Practices
# ------------------------------------------------------------------------------
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = "DENY"

    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True

    # HSTS
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# ------------------------------------------------------------------------------
# DEFAULT PRIMARY KEY
# ------------------------------------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
