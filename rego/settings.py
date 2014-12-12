import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    STRIPE_KEY = os.environ.get('STRIPE_KEY')
    STRIPE_PUBLIC_KEY = os.environ.get('STRIPE_PUBLIC_KEY')


class ProdConfig(object):
    DEBUG = False


class DevConfig(object):
    DEBUG = True
    SECRET_KEY = 'nosecret'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'
