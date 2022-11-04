"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 4.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-m4wa_k1=aek%5gmxw4b3u%(&*lt)k$(2=6zo(el7ffwr@xoh&8'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'home.apps.HomeConfig',
    'mana.apps.ManaConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'mana.middleware.perm.PermMiddleware',
]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default":{
        "ENGINE":"django.db.backends.mysql",
        "NAME":"family",
        "USER":"totem_user",
        "PASSWORD":"totem123",
        "HOST":"39.107.248.28",
        "PORT":"9000",
        "OPTIONS":{'charset':'utf8mb4'}
    },
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

SERVER_DATABASE = "family"
SERVER_USER = "totem_user"
SERVER_PASSWORD = "totem123"
SERVER_HOST = "39.107.248.28"
SERVER_PORT = 9000

LOCAL_DATABASE = "family"
LOCAL_USER = "postgres"
LOCAL_PASSWORD = "123456"
LOCAL_HOST = "localhost"
LOCAL_PORT = 5432

RESOURCE_PATH = os.path.join(os.path.abspath('.'), "resources")
PDF_OUTPUT_PATH = os.path.join(os.path.abspath('.'), "output")

MAX_ROW_STR = 26  # 每行最多的字符数  # 35
MAX_LINE = 40  # 行传每页最多的行数  # 47

MAX_LINE_TREE = 25  # 吊线图每页最多的行数

image_path = os.path.join(os.path.abspath('.'), "resources", "image")
IMAGE_PATH = image_path.replace('\\', '/')
WK_PATH = '/usr/local/bin/wkhtmltopdf'


PRESET_DOC_TYPE = ["凡例", "源流", "文献", "人物事迹", "家族事件", "公德榜", "附录", "后记"]

PERSON_ATTRIBUTE = ['id', 'family_name', 'name', 'zi', 'hao', 'sex', 'generation', 'ranknum', 'isliving', 'date_birth',
                    'date_dead', 'education', 'title_post', 'desc_living', 'desc_dead', 'father_id', 'zp_id']

PERSON_ATTRIBUTE_INDEX = [9, 10, 13, 14]

GENERATION_OPTIONS = {
    "father": "{0}{1}{2}；",  # 格式例：礼周 长 子
    "zi": "字：{}；",
    "hao": "号：{}；\n",

    "spouse": "娶妻：{}\n",
    "son": "子{}：{}\n",  # 格式例：子 二：兴元 兴知
    "daughter": "女{}：{}\n",  # 格式例：同上

    "date_birth": "生于{}；",
    "date_dead": "卒于{}；\n",

    "education": "教育程度：{}；",
    "title_post": "曾任：{}；\n",

    "desc_living": "{}\n",
    "desc_dead": "{}\n"
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
# STATIC_ROOT = (
#     os.path.join(BASE_DIR, 'static'),
#     os.path.join(BASE_DIR, 'home/static'),
#     os.path.join(BASE_DIR, 'mana/static'),
# )
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# 定义session 键：
# 保存用户权限url列表
# 保存 权限菜单 和所有 菜单
SESSION_PERMISSION_URL_KEY = 'cool'

SESSION_MENU_KEY = 'awesome'
ALL_MENU_KEY = 'k1'
PERMISSION_MENU_KEY = 'k2'

LOGIN_URL = '/login/'

REGEX_URL = r'^{url}$'  # url作严格匹配

# 配置url权限白名单
SAFE_URL = [
    r'/login/',
    r'/regist/',
    '/admin/.*',
    '/test/',
    '/',
    '^/mana/',
    '/static/.*',
]
