from pathlib import Path

logger = logging.getLogger(__name__)

BASE_DIR = "./src"

# SECRET_KEY = os.getenv(
#    "DJANGO_SECRET_KEY",
#    "django-insecure-y%tyxe6l41i*rrzsxpf45kse%4lh4xqz0o74k^_icgfo(htv(t",
# )

# ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")

INSTALLED_APPS = [
    "django.contrib.admin",
    #    "django.contrib.auth",
    #    "django.contrib.contenttypes",
    #    "django.contrib.sessions",
    #    "django.contrib.messages",
    #    "django.contrib.staticfiles",
]

# MIDDLEWARE = [
#    "django.middleware.security.SecurityMiddleware",
#    "django.contrib.sessions.middleware.SessionMiddleware",
#    "django.middleware.common.CommonMiddleware",
#    "django.middleware.csrf.CsrfViewMiddleware",
#    "django.contrib.auth.middleware.AuthenticationMiddleware",
#    "django.contrib.messages.middleware.MessageMiddleware",
#    "django.middleware.clickjacking.XFrameOptionsMiddleware",
# ]
#
# TEMPLATES = [
#    {
#        "BACKEND": "django.template.backends.django.DjangoTemplates",
#        "DIRS": [Path(__file__).resolve().parent / "templates"],
#        "APP_DIRS": True,
#        "OPTIONS": {
#            "context_processors": [
#                "django.template.context_processors.request",
#                "django.contrib.auth.context_processors.auth",
#                "django.contrib.messages.context_processors.messages",
#            ],
#        },
#    },
# ]
#
# AUTH_PASSWORD_VALIDATORS = [
#    {
#        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
#    },
#    {
#        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
#    },
#    {
#        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
#    },
#    {
#        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
#    },
# ]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# STATIC_URL = "/static/"
# STATIC_ROOT = "../generated/"
# STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
#
# DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
#
# LOGGING = {
#    "version": 1,
#    "disable_existing_loggers": False,
#    "formatters": {
#        "simple": {
#            "format": "%(asctime)s %(levelname)-8s: %(message)",
#        },
#        "verbose": {
#            "format": "%(asctime)s %(levelname)-8s %(name)-20s: %(message)s",
#        },
#    },
#    "handlers": {
#        "console": {
#            "class": "logging.StreamHandler",
#            "formatter": os.getenv("DJANGO_LOG_FORMAT", "verbose"),
#        },
#    },
#    "root": {"handlers": ["console"], "propagate": False, "level": "WARNING"},
#    "loggers": {
#        "cis": {
#            "handlers": ["console"],
#            "propagate": False,
#            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
#        },
#        "ptl_gina": {
#            "handlers": ["console"],
#            "propagate": False,
#            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
#        },
#    },
# }
#
# REST_FRAMEWORK = {
#    "DEFAULT_PAGINATION_CLASS": "cis.api.pager.LargeResultsSetPagination",
#    "DEFAULT_FILTER_BACKENDS": [
#        "django_filters.rest_framework.DjangoFilterBackend",
#        "rest_framework.filters.OrderingFilter",
#        "rest_framework.filters.SearchFilter",
#    ],
#    "DEFAULT_PERMISSION_CLASSES": [
#        "rest_framework.permissions.AllowAny",
#    ],
#    "DEFAULT_AUTHENTICATION_CLASSES": (
#        "rest_framework.authentication.BasicAuthentication",
#    ),
# }
#
# AUTHENTICATION_BACKENDS = ("django.contrib.auth.backends.ModelBackend",)
#
# LOGIN_URL = "/api/auth/login/"
