"""
ローカル環境で適用される設定内容
"""
from .base import *


env = environ.Env()
environ.Env.read_env(env_file=str(BASE_DIR) + "/.env")

SECRET_KEY = env("SECRET_KEY")

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    "default": env.db(),
}

# ローカル環境のみ設定
INSTALLED_APPS.insert(0, 'whitenoise.runserver_nostatic')

CLOUDINARY_STORAGE  = {
    'CLOUD_NAME':'hip3gt8kc',
    'API_KEY': env('CLOUDINARY_API_KEY'),
    'API_SECRET': env('CLOUDINARY_API_SECRET')
}