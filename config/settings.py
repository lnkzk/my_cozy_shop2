from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-super-secret-key-for-koti-shop'
DEBUG = True
ALLOWED_HOSTS = ['lnkzk.pythonanywhere.com', '127.0.0.1', 'localhost']

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'shop.apps.ShopConfig',
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
WSGI_APPLICATION = 'config.wsgi.application'

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
                'shop.context_processors.cart',
                'shop.context_processors.header_data',
            ],
        },
    },
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Minsk'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

CART_SESSION_ID = 'cart'

JAZZMIN_SETTINGS = {
    "site_title": "KÓTI Admin",
    "site_header": "KÓTI",
    "site_brand": "KÓTI Эстетика",
    "welcome_sign": "Добро пожаловать в панель управления KÓTI",
    "hide_models": ["shop.Color", "shop.Purpose", "shop.OrderFormField"],
    "order_with_respect_to": [
        "shop.Order", "shop.Product", "shop.Category", "shop.PriceUpdate",
        "shop.Courier", "shop.WorkingSchedule", "shop.DeliveryMethod", "shop.PaymentMethod",
        "shop.MainBanner", "shop.PromoBanner", "shop.CategoryBlockSettings",
        "shop.FeaturedProductsSettings", "shop.HeaderSettings", "shop.HeaderNavigation", "shop.FooterSettings",
    ],
    "icons": {
        "shop.Order": "fas fa-shopping-bag", "shop.Product": "fas fa-box",
        "shop.Category": "fas fa-tags", "shop.PriceUpdate": "fas fa-file-excel",
        "shop.Courier": "fas fa-user-ninja", "shop.WorkingSchedule": "fas fa-clock",
        "shop.DeliveryMethod": "fas fa-truck", "shop.PaymentMethod": "fas fa-credit-card",
        "shop.MainBanner": "fas fa-image", "shop.PromoBanner": "fas fa-percent",
        "shop.CategoryBlockSettings": "fas fa-th-large", "shop.FeaturedProductsSettings": "fas fa-star",
        "shop.HeaderSettings": "fas fa-heading", "shop.HeaderNavigation": "fas fa-bars",
        "shop.FooterSettings": "fas fa-shoe-prints",
    },
}


# НАСТРОЙКИ ПОЧТЫ GMAIL ДЛЯ УВЕДОМЛЕНИЙ
# ==============================================================================
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'aicreator045@gmail.com'  # <-- Впиши сюда именно ту почту, с которой ты сейчас создала этот пароль
EMAIL_HOST_PASSWORD = 'jnxddedsutbbrnnz'  # <-- Тот самый пароль со скриншота (я уже убрал из него пробелы, так и нужно)