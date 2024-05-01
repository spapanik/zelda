import contextlib
import pathlib
from functools import partial

import django_stubs_ext
from dj_settings import get_setting

BASE_DIR = pathlib.Path(__file__).parents[2]
PROJECT_DIR = BASE_DIR.joinpath("src")
project_setting = partial(get_setting, project_dir=BASE_DIR, filename="zelda.yml")
django_stubs_ext.monkeypatch()

# region Security
validation = "django.contrib.auth.password_validation"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": f"{validation}.UserAttributeSimilarityValidator"},
    {"NAME": f"{validation}.MinimumLengthValidator"},
    {"NAME": f"{validation}.CommonPasswordValidator"},
    {"NAME": f"{validation}.NumericPasswordValidator"},
]

SECRET_KEY = project_setting(
    "SECRET_KEY",
    sections=["project", "security"],
    default="Insecure:fXP7kny5q3oKDV6_yBjs-keX6oZfRqC9pz--LDJ42r8",
)
BASE_SCHEME = project_setting(
    "BASE_SCHEME", sections=["project", "security"], default="https"
)
if BASE_SCHEME == "https":
    SECURE_PROXY_SSL_HEADER = "HTTP_X_FORWARDED_PROTO", "https"
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
# endregion

# region Application definition
DEBUG = project_setting("DEBUG", sections=["project", "app"], rtype=bool, default=True)
BASE_DOMAIN = project_setting(
    "BASE_DOMAIN", sections=["project", "servers"], default="localhost"
)
BASE_PORT = project_setting(
    "BASE_PORT", sections=["project", "servers"], rtype=int, default=8000
)
EXTRA_DOMAINS = project_setting(
    "EXTRA_DOMAINS", sections=["project", "servers"], rtype=list, default=["127.0.0.1"]
)
ALLOWED_HOSTS = [BASE_DOMAIN, *EXTRA_DOMAINS]

AUTH_USER_MODEL = "registration.User"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
ROOT_URLCONF = "zelda.urls"

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "zelda.branding",
    "grappelli.dashboard",
    "grappelli",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "zelda.lib",
    "zelda.registration",
    "zelda.armor",
    "zelda.home",
]

if DEBUG:
    INSTALLED_APPS += [
        "django_extensions",
    ]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

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
            ]
        },
    }
]

EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = BASE_DIR.joinpath("local", "emails")

MIGRATION_HASHES_PATH = BASE_DIR.joinpath("migrations.lock")

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"
# endregion

# region Databases
DATABASES = {
    "default": {"ENGINE": "django.db.backends.postgresql", "NAME": "zelda"},
}
# endregion

# region Static files
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"
    },
}
# endregion

# region Static files
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR.joinpath(".static")
# endregion

# region i18n/l10n
LANGUAGE_CODE = "en"
LANGUAGES = [("en", "English")]
# endregion

# region 3rd party
GRAPPELLI_INDEX_DASHBOARD = "zelda.home.dashboard.AdminDashboard"
GRAPPELLI_ADMIN_TITLE = "zelda"
# endregion

with contextlib.suppress(ImportError):
    from zelda.local.settings import *  # noqa: F403
