"""
Django settings for example_project project.

Generated by 'django-admin startproject' using Django 2.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "tpye0s&&$uyc)hf_3rv@!a95ne*3e-dxt^9k^7!f+$jxkk+$k-"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.humanize",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    # punkweb_boards apps
    "compressor",
    "easy_thumbnails",
    "rest_framework",
    "precise_bbcode",
    "punkweb_boards",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # punkweb_boards middleware
    "punkweb_boards.middleware.ActiveUserMiddleware",
]

ROOT_URLCONF = "example_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "example_project/templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # punkweb_boards context_processors
                "punkweb_boards.context_processors.settings",
                "punkweb_boards.context_processors.base_context",
            ]
        },
    }
]

WSGI_APPLICATION = "example_project.wsgi.application"


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DATABASE_NAME", "punkweb_boards"),
        "USER": os.environ.get("DATABASE_USER", "punkweb_boards"),
        "PASSWORD": os.environ.get("DATABASE_PASSWORD", "punkweb_boards"),
        "HOST": os.environ.get("DATABASE_HOST", "db"),
        "PORT": "5432",
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = "/static/"
MEDIA_URL = "/media/"

STATIC_ROOT = os.path.join(BASE_DIR, "server", "dev", "static")
MEDIA_ROOT = os.path.join(BASE_DIR, "server", "dev", "media")

STATIC_DIR = os.path.join(BASE_DIR, "example_project/static")

STATICFILES_DIRS = (STATIC_DIR,)

# TODO: Figure out if compressor is required to be configured for
# projects using punkweb_boards

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
)

COMPRESS_PRECOMPILERS = (("text/x-scss", "django_libsass.SassCompiler"),)

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Set these if you want to login through punkweb_boards

LOGIN_REDIRECT_URL = "/board/"
LOGOUT_REDIRECT_URL = "/board/"

# This is required for punkweb_boards to track who is online or when they were last seen

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.memcached.PyMemcacheCache",
        "LOCATION": os.environ.get("MEMCACHED_HOST", "cache") + ":11211",
    }
}

# Everything below is required for punkweb_boards

THUMBNAIL_ALIASES = {
    "": {
        "avatar": {"size": (200, 200), "crop": True},
        "avatar_small": {"size": (100, 100), "crop": True},
        "avatar_smaller": {"size": (50, 50), "crop": True},
        "avatar_smallest": {"size": (25, 25), "crop": True},
    }
}

PUNKWEB_BOARDS = {
    "BOARD_NAME": "Example",
}
