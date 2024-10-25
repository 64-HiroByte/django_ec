"""
本番環境(Heroku）で適用される設定内容
"""
from .base import *


# env = environ.Env()

SECRET_KEY = env("SECRET_KEY")

DEBUG = False

ALLOWED_HOSTS = ['.herokuapp.com']

DATABASES = {
    "default": env.db(),
}

CLOUDINARY_STORAGE  = {
    'CLOUD_NAME':'hip3gt8kc',
    'API_KEY': env('CLOUDINARY_API_KEY'),
    'API_SECRET': env('CLOUDINARY_API_SECRET')
}