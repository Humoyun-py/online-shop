"""
Django sozlamalari - E-Commerce do'kon
"""

from pathlib import Path

# Asosiy papka yo'li
BASE_DIR = Path(__file__).resolve().parent.parent

# Xavfsizlik kaliti - ishlab chiqarishda o'zgartiring!
SECRET_KEY = 'django-insecure-$^(00z7_8h$0yjufz6)(^vzt)cp2e1r@ve2bbp099@wc6f^+qd'

# Debug rejim - productionoda False qiling
DEBUG = True

ALLOWED_HOSTS = ['*']

# O'rnatilgan ilovalar
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'shop',  # Bizning do'kon ilovasi
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

ROOT_URLCONF = 'config.urls'

# Template sozlamalari
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'config.wsgi.application'

# Ma'lumotlar bazasi - SQLite
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Parol tekshirish
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Til va zona sozlamalari
LANGUAGE_CODE = 'uz'
TIME_ZONE = 'Asia/Tashkent'
USE_I18N = True
USE_TZ = True

# Statik fayllar sozlamalari
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media fayllar (mahsulot rasmlari)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Login yo'naltirish
LOGIN_URL = '/kirish/'
LOGIN_REDIRECT_URL = '/'

# Default primary key
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
