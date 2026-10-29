import os
from pathlib import Path

import dj_database_url
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# Configurações de ambiente ficam fora do código para facilitar diferentes ambientes.
# O valor real deve ficar no arquivo .env e nunca ser versionado.
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-only-change-me")
DEBUG = os.getenv("DJANGO_DEBUG", "True").lower() == "true"
ALLOWED_HOSTS = [host.strip() for host in os.getenv("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",") if host.strip()]

# Em produção, DATABASE_URL deve apontar para o PostgreSQL hospedado.
# Sem ela, o fallback localhost só funciona no computador de desenvolvimento.
if not DEBUG and not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL precisa ser configurada quando DJANGO_DEBUG=False.")

# Cada app instalado pode fornecer modelos, views, comandos e arquivos administrativos.
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "inventario.assets",
]

# Middleware são etapas executadas em cada requisição, como sessão, CSRF e autenticação.
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "inventario.urls"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {"context_processors": [
            "django.template.context_processors.request",
            "django.contrib.auth.context_processors.auth",
            "django.contrib.messages.context_processors.messages",
        ]},
    }
]
WSGI_APPLICATION = "inventario.wsgi.application"

# PostgreSQL é o banco oficial do projeto; as variáveis vêm do arquivo .env.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", "inventario"),
        "USER": os.getenv("POSTGRES_USER", "postgres"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "postgres"),
        "HOST": os.getenv("POSTGRES_HOST", "localhost"),
        "PORT": os.getenv("POSTGRES_PORT", "5432"),
    }
}
# SQLite facilita o desenvolvimento local; em homologação/produção o padrão é PostgreSQL.
if os.getenv("USE_SQLITE", "False").lower() == "true":
    sqlite_path = Path(os.getenv("SQLITE_PATH", BASE_DIR / "data" / "inventario.sqlite3"))
    sqlite_path.parent.mkdir(parents=True, exist_ok=True)
    DATABASES["default"] = {"ENGINE": "django.db.backends.sqlite3", "NAME": sqlite_path}

LANGUAGE_CODE = "pt-br"
# Plataformas de hospedagem normalmente entregam o PostgreSQL em DATABASE_URL.
if os.getenv("DATABASE_URL"):
    DATABASES["default"] = dj_database_url.parse(os.environ["DATABASE_URL"], conn_max_age=600, ssl_require=not DEBUG)
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
LOGIN_URL = "assets:login"
LOGIN_REDIRECT_URL = "assets:dashboard"
LOGOUT_REDIRECT_URL = "assets:login"
