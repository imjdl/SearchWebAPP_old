"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 1.11.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 't=ltrz%59$f=ty)!t-rmi8f^1k*%kvg^osneyx36h(421xde@q'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
ALLOWED_HOSTS = ["*",]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'searchapp',
    'search_manager',
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

ROOT_URLCONF = 'mysite.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {

        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ENGINE': "django.db.backends.mysql",
        "NAME": "SearchApp",
        "HOST": "127.0.0.1",
        "PORT": "3306",
        "OPTIONS":{
            "init_command":"SET sql_mode='STRICT_TRANS_TABLES'"
        },
        "USER": "elloit",
        "PASSWORD": "elloit"
    }
}
# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "collect_static")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

# upload folder
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# 发送邮件设置

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_USE_TLS = True   #是否使用TLS安全传输协议
EMAIL_USE_SSL = False
EMAIL_HOST = 'smtp.163.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = '18238670823@163.com'
EMAIL_HOST_PASSWORD = 'j123456'
DEFAULT_FROM_EMAIL = 'SearchApp网络空间搜索引擎<18238670823@163.com>'

# CSRF_SESSION 设置
CSRF_COOKIE_HTTPONLY = True

# Session 设置
# SESSION_CACHE_ALIAS = 'default'                         # Cache to store session data if using the cache session backend.
# SESSION_COOKIE_NAME = ''                       # Cookie name. This can be whatever you want.
# SESSION_COOKIE_AGE = 60 * 5                             # Age of cookie, in seconds (default: 2 weeks). Now is 5 minutes.
# SESSION_COOKIE_DOMAIN = None                            # A string like ".example.com", or None for standard domain cookie.
# SESSION_COOKIE_SECURE = False                           # Whether the session cookie should be secure (https:// only).
# SESSION_COOKIE_PATH = '/'                               # The path of the session cookie.
SESSION_COOKIE_HTTPONLY = True                          # Whether to use the non-RFC standard httpOnly flag (IE, FF3+, others)
# SESSION_SAVE_EVERY_REQUEST = Fals
# e                      # Whether to save the session data on every request.
# SESSION_EXPIRE_AT_BROWSER_CLOSE = True                  # Whether a user's session cookie expires when the Web browser is closed.
# SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # The module to store session data
# SESSION_FILE_PATH = None                                # Directory to store session files if using the file session module. If None, the backend will use a sensible default.
# SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'  # class to serialize session data