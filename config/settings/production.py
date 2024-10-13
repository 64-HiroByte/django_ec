from .base import *


env = environ.Env()

SECRET_KEY = env("SECRET_KEY")

DEBUG = False

ALLOWED_HOSTS = ['.heroku.com']

DATABASES = {
    "default": env.db(),
}

MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
