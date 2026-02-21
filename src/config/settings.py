from __future__ import annotations

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "change-me")
DEBUG = os.getenv("DJANGO_DEBUG", "false").lower() == "true"
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "*").split(",")

SHARED_APPS = [
    "django_tenants",
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.admin",
    "django_prometheus",
    "rest_framework",
    "drf_spectacular",
    "apps.common",
    "apps.tenancy",
    "apps.accounts",
]

TENANT_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.admin",
    "rest_framework",
    "drf_spectacular",
    "apps.common",
    "apps.projects",
]

INSTALLED_APPS = SHARED_APPS + [a for a in TENANT_APPS if a not in SHARED_APPS]

TENANT_MODEL = "tenancy.Client"
TENANT_DOMAIN_MODEL = "tenancy.Domain"

MIDDLEWARE = [
    "django_prometheus.middleware.PrometheusBeforeMiddleware",
    "django_tenants.middleware.main.TenantMainMiddleware",
    "apps.tenancy.middleware.HybridTenantMiddleware",
    "apps.common.middleware.StructuredRequestLogMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_prometheus.middleware.PrometheusAfterMiddleware",
]

ROOT_URLCONF = "config.urls"
PUBLIC_SCHEMA_URLCONF = "config.urls_public"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django_tenants.postgresql_backend",
        "NAME": os.getenv("POSTGRES_DB", "hybrid_saas"),
        "USER": os.getenv("POSTGRES_USER", "postgres"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "postgres"),
        "HOST": os.getenv("POSTGRES_HOST", "localhost"),
        "PORT": int(os.getenv("POSTGRES_PORT", "5432")),
        "CONN_MAX_AGE": 60,
    },
    "dedicated": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DEDICATED_DB", "hybrid_saas_dedicated"),
        "USER": os.getenv("POSTGRES_DEDICATED_USER", os.getenv("POSTGRES_USER", "postgres")),
        "PASSWORD": os.getenv("POSTGRES_DEDICATED_PASSWORD", os.getenv("POSTGRES_PASSWORD", "postgres")),
        "HOST": os.getenv("POSTGRES_DEDICATED_HOST", os.getenv("POSTGRES_HOST", "localhost")),
        "PORT": int(os.getenv("POSTGRES_DEDICATED_PORT", os.getenv("POSTGRES_PORT", "5432"))),
        "CONN_MAX_AGE": 60,
    },
}
DATABASE_ROUTERS = ["apps.tenancy.db_router.TenantDatabaseRouter"]
DATABASE_URL = DATABASES["default"]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Hybrid SaaS API",
    "DESCRIPTION": "Hybrid multi-tenant backend with row-based and schema-based isolation.",
    "VERSION": "1.0.0",
}

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": REDIS_URL,
    }
}

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", REDIS_URL)
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", REDIS_URL)
CELERY_TASK_ALWAYS_EAGER = os.getenv("CELERY_TASK_ALWAYS_EAGER", "false").lower() == "true"
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_ACCEPT_CONTENT = ["json"]

AUTH_USER_MODEL = "accounts.User"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "fmt": "%(asctime)s %(levelname)s %(name)s %(message)s %(pathname)s %(lineno)d",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "json",
        }
    },
    "root": {"handlers": ["console"], "level": os.getenv("DJANGO_LOG_LEVEL", "INFO")},
}

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
CSRF_TRUSTED_ORIGINS = [origin for origin in os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",") if origin]
