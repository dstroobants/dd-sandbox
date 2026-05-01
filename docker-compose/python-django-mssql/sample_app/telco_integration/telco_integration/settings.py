"""
Django settings for telco_integration project.

Mirrors the layout of the production application (Django 3.2). For the full
list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-dev-key-do-not-use-in-prod")

DEBUG = os.environ.get("DEBUG", "True").lower() in ("1", "true", "yes")

ALLOWED_HOSTS = ["*"]


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    # OpenCensus middleware first so it wraps the entire request lifecycle,
    # exactly the way it is wired in production (opencensus-ext-django==0.8.0).
    # Running OpenCensus + Datadog tracers side-by-side under gevent is a known
    # deadlock trigger: both libraries use real `threading.Lock`s for their
    # exporter/writer threads while the request itself runs in a greenlet.
    "opencensus.ext.django.middleware.OpencensusMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# OpenCensus configuration. Production uses opencensus-ext-azure (Azure
# Monitor exporter); the print exporter is used locally so we don't need an
# Azure connection string. The behaviour that matters (a second tracing
# pipeline with its own background exporter thread + locks) is the same.
OPENCENSUS = {
    "TRACE": {
        "SAMPLER": "opencensus.trace.samplers.ProbabilitySampler(rate=1.0)",
        "EXPORTER": "opencensus.trace.print_exporter.PrintExporter()",
    },
}

ROOT_URLCONF = "telco_integration.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "telco_integration.wsgi.application"


# MSSQL via mssql-django + pyodbc, matching the production stack.
# Connection params come from env vars set in docker-compose.yml.
DATABASES = {
    "default": {
        "ENGINE": "mssql",
        "NAME": os.environ.get("DB_NAME", "tempdb"),
        "USER": os.environ.get("DB_USER", "sa"),
        "PASSWORD": os.environ.get("DB_PASSWORD", "YourStrong!Passw0rd"),
        "HOST": os.environ.get("DB_HOST", "mssql"),
        "PORT": os.environ.get("DB_PORT", "1433"),
        "OPTIONS": {
            "driver": "ODBC Driver 18 for SQL Server",
            "extra_params": "TrustServerCertificate=yes;Encrypt=yes",
        },
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = "/static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Mirrors the production structlog-flavoured logging so trace_id/span_id
# injection (DD_LOGS_INJECTION=true) has somewhere to land. Kept basic on
# purpose.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(asctime)s %(levelname)s %(name)s %(message)s "
                      "[dd.trace_id=%(dd.trace_id)s dd.span_id=%(dd.span_id)s "
                      "dd.service=%(dd.service)s dd.env=%(dd.env)s]",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}
