import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-cozy-lumora-secret-key-change-this-in-production'

DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'shop',
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

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # ИСПРАВЛЕНО: Возвращены оба процессора данных для корзины и шапки KOTI
                'shop.context_processors.cart',
                'shop.context_processors.header_data',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Minsk'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

JAZZMIN_SETTINGS = {
    "site_title": "Панель управления KÓTI",
    "site_header": "KÓTI Панель",
    "site_brand": "KÓTI Эстетика",
    "welcome_sign": "Панель управления интернет-магазином KÓTI",
    "copyright": "KÓTI Home Goods",
    "search_model": ["shop.Product"],
    "user_avatar": None,
    "topmenu_links": [
        {"name": "Перейти на сайт", "url": "shop:product_list", "new_window": True},
    ],
    "show_sidebar": True,
    "navigation_expanded": True,
    "icons": {
        "auth.User": "fas fa-user-shield",
        "auth.Group": "fas fa-users",
        "shop.Order": "fas fa-shopping-bag",
        "shop.Product": "fas fa-tags",
        "shop.Category": "fas fa-th-list",
        "shop.MainBanner": "fas fa-image",
        "shop.PromoBanner": "fas fa-percent",
        "shop.FeaturedProductsSettings": "fas fa-star",
        "shop.CategoryBlockSettings": "fas fa-shapes",
        "shop.HeaderSettings": "fas fa-cog",
        "shop.HeaderNavigation": "fas fa-bars",
        "shop.FooterSettings": "fas fa-shoe-prints",
    },
    "order_with_respect_to": [
        "shop.Order", "shop.Product", "shop.Category", "shop.MainBanner",
        "shop.CategoryBlockSettings", "shop.PromoBanner", "shop.FeaturedProductsSettings",
        "shop.HeaderSettings", "shop.HeaderNavigation", "shop.FooterSettings", "auth"
    ],
    "changeform_format": "horizontal_tabs",
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False, "footer_small_text": False, "body_small_text": False, "brand_small_text": False,
    "brand_colour": "navbar-dark", "accent": "accent-teal", "navbar": "navbar-dark bg-dark", "no_navbar_border": False,
    "navbar_fixed": False, "layout_options": { "sidebar_fixed": True, "sidebar_mini": False, "footer_fixed": False, "dark_mode_top_nav": False, "dark_mode_sidebar": True },
    "sidebar": "sidebar-dark-teal", "sidebar_nav_small_text": False, "sidebar_disable_expand": False, "sidebar_nav_child_indent": True, "sidebar_nav_compact_style": False, "sidebar_nav_legacy_style": False, "sidebar_nav_flat_style": False, "theme": "flatly"
}

CART_SESSION_ID = 'cart'