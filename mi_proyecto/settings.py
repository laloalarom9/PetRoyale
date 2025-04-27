import os
import dj_database_url
from pathlib import Path



BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-6vl06(3ti$*_c%0lb5390qvmwf1imvlv16ncsqz5&p)*u!@llv"

DEBUG = False  # 🔹 Cambiar a False en producción

ALLOWED_HOSTS = ["petroyale-ehg7gyadd4h6c7gk.spaincentral-01.azurewebsites.net", "127.0.0.1"]

LOGIN_URL = '/login/'


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "whitenoise.runserver_nostatic",  # Debe estar en la lista
    "mi_proyecto",
    'crispy_forms',
    'crispy_bootstrap5',
]
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Debe estar antes de SessionMiddleware
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "mi_proyecto.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "mi_proyecto.context_processors.avatar_context",  # Usa mi_proyecto en lugar de una app
                "mi_proyecto.context_processors.user_groups_processor",  # 🔹 Agregar aquí

            ],
        },
    },
]



AUTH_USER_MODEL = 'mi_proyecto.CustomUser'  # Cambia "mi_proyecto" por el nombre real de tu app

WSGI_APPLICATION = "mi_proyecto.wsgi.application"

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


# 🚀 Poner DEBUG en True temporalmente
DEBUG = True  # Cambiar a False solo en producción

# Configuración de archivos estáticos
STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("PGDATABASE", "postgres"),  # Nombre de la base de datos
        "USER": os.getenv("PGUSER", "petroyale"),  # Usuario de PostgreSQL
        "PASSWORD": os.getenv("PGPASSWORD", "Libert@d25"),  # Contraseña de PostgreSQL
        "HOST": os.getenv("PGHOST", "petroyalebd.postgres.database.azure.com"),  # Servidor en Azure
        "PORT": os.getenv("PGPORT", "5432"),  # Puerto de PostgreSQL
        "OPTIONS": {"sslmode": "require"},  # Azure requiere SSL
    }#
}


#  SEGURIDAD EN PRODUCCIÓN
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
CSRF_TRUSTED_ORIGINS = ["https://petroyale-ehg7gyadd4h6c7gk.spaincentral-01.azurewebsites.net"]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"



EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "petroyale55@gmail.com"  # Reemplázalo con tu correo de Gmail
EMAIL_HOST_PASSWORD = "slem pwdx acny pclb"  # ⚠ Pon tu contraseña aquí (No recomendado)
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

GOOGLE_MAPS_API_KEY = 'AIzaSyBYNP4mbrKHHFxP3t5E-11Sl6cFYkzJ0es'


