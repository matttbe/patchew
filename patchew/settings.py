#!/usr/bin/env python3
#
# Copyright 2016 Red Hat, Inc.
#
# Authors:
#     Fam Zheng <famz@redhat.com>
#
# This work is licensed under the MIT License.  Please see the LICENSE file or
# http://opensource.org/licenses/MIT.

"""
Django settings for patchew project.

Generated by 'django-admin startproject' using Django 1.9.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

VERSION = open(os.path.join(BASE_DIR, "VERSION"), "r").read().strip()

MODULE_DIR = os.path.join(BASE_DIR, "mods")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "@f-l5@70om7o(7rda^oxd$f#60g3jy#&m^p7z@vkf+&$*@%!^o"

X_FRAME_OPTIONS = "SAMEORIGIN"

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    "api.apps.ApiConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "rest_auth",
    "rest_framework",
    "rest_framework.authtoken",
]

MIDDLEWARE = [
    "django.middleware.gzip.GZipMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
        "patchew.CsrfExemptSessionAuthentication",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "URL_FIELD_NAME": "resource_uri",
    "PAGE_SIZE": 50,
    "UPLOADED_FILES_USE_URL": True,
}

ROOT_URLCONF = "patchew.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "www", "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "builtins": ["patchew.tags"],
        },
    }
]

WSGI_APPLICATION = "patchew.wsgi.application"


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases


def env_detect():
    if "PATCHEW_DB_PORT_5432_TCP_ADDR" in os.environ:
        # Docker deployment
        return (
            False,
            os.environ.get("PATCHEW_DATA_DIR"),
            {
                "default": {
                    "ENGINE": "django.db.backends.postgresql",
                    "NAME": "patchew",
                    "USER": "patchew",
                    "PASSWORD": "patchew",
                    "HOST": os.environ.get("PATCHEW_DB_PORT_5432_TCP_ADDR"),
                    "PORT": "5432",
                }
            },
        )
    elif "VIRTUAL_ENV" in os.environ or os.environ.get("PATCHEW_DEBUG", False):
        # Development setup
        data_dir = os.path.join(
            os.environ.get("VIRTUAL_ENV", "/var/tmp/patchew-dev"), "data"
        )
        return (
            True,
            data_dir,
            {
                "default": {
                    "ENGINE": "django.db.backends.sqlite3",
                    "NAME": os.path.join(data_dir, "patchew-db.sqlite3"),
                }
            },
        )
    else:
        raise Exception("Unknown running environment")


DEBUG, DATA_DIR, DATABASES = env_detect()

if DATABASES["default"]["ENGINE"] == "django.db.backends.postgresql":
    INSTALLED_APPS += ["django.contrib.postgres"]

# In production environments, we run in a container, behind nginx, which should
# filter the allowed host names and block large requests. So be a little flexible here
ALLOWED_HOSTS = ["*"]
DATA_UPLOAD_MAX_MEMORY_SIZE = None

if not os.path.isdir(DATA_DIR):
    os.makedirs(DATA_DIR)

BLOB_DIR = os.path.join(DATA_DIR, "blob")
if not os.path.isdir(BLOB_DIR):
    os.mkdir(BLOB_DIR)

if DEBUG:
    INSTALLED_APPS += ["debug_toolbar"]
    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

MEDIA_ROOT = os.path.join(DATA_DIR, "media")
MEDIA_URL = "/media/"

if not os.path.isdir(MEDIA_ROOT):
    os.makedirs(MEDIA_ROOT)

# If the PATCHEW_ADMIN_EMAIL env var is set, let Django send error reporting to
# the address.
admin_email = os.environ.get("PATCHEW_ADMIN_EMAIL")
if admin_email:
    ADMINS = [("admin", admin_email)]

SERVER_EMAIL = "server@patchew.org"

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = "/static/"

STATIC_ROOT = os.path.join(BASE_DIR, "wsgi", "static")

STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

INTERNAL_IPS = ["127.0.0.1"]

if not DEBUG:
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {
            "file": {
                "level": "DEBUG",
                "class": "logging.FileHandler",
                "filename": os.path.join(DATA_DIR, "log", "patchew.log"),
            },
            "null": {"level": "DEBUG", "class": "logging.NullHandler"},
        },
        "loggers": {
            "django": {"handlers": ["file"], "level": "DEBUG", "propagate": True},
            "django.template": {
                "handlers": ["null"],  # Quiet by default!
                "propagate": False,
                "level": "DEBUG",
            },
        },
    }
