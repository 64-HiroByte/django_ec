"""
ローカル環境で適用される設定内容
"""
from .base import *


environ.Env.read_env(env_file=str(BASE_DIR) + "/.env")

SECRET_KEY = env("SECRET_KEY")

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    "default": env.db(),
}

# ローカル環境のみ設定
INSTALLED_APPS.insert(0, 'whitenoise.runserver_nostatic')

# Cloudinaryの設定
CLOUDINARY_STORAGE  = {
    'CLOUD_NAME': env('CLOUD_NAME'),
    'API_KEY': env('CLOUDINARY_API_KEY'),
    'API_SECRET': env('CLOUDINARY_API_SECRET')
}

# basic認証
BASICAUTH_USERS = {env('BASICAUTH_USER_NAME'): env('BASICAUTH_PASSWORD')}
# SendGridのAPIキー
EMAIL_HOST_PASSWORD = env('SENDGRID_API_KEY')

# 開発環境において、メール送信はコンソールに出力
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

'''
#########################################################################

django-debug-toolbarの設定

#########################################################################
'''
def show_toolbar(request):
    return True


INSTALLED_APPS += [
    'debug_toolbar',
]
MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]
DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': show_toolbar,
}
