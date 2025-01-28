"""
本番環境(Heroku）で適用される設定内容
"""
from .base import *


SECRET_KEY = env("SECRET_KEY")

DEBUG = False

ALLOWED_HOSTS = ['.herokuapp.com']

DATABASES = {
    "default": env.db(),
}

CLOUDINARY_STORAGE  = {
    'CLOUD_NAME': env('CLOUD_NAME'),
    'API_KEY': env('CLOUDINARY_API_KEY'),
    'API_SECRET': env('CLOUDINARY_API_SECRET')
}

# basic認証
BASICAUTH_USERS = {env('BASICAUTH_USER_NAME'): env('BASICAUTH_PASSWORD')}

# SendGridのAPIキー
EMAIL_HOST_PASSWORD = env('SENDGRID_API_KEY')
# メール送信元のアドレス
FROM_EMAIL_ADDRESS = env('EMAIL_ADDRESS')