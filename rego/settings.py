class Config(object):
    pass


class ProdConfig(object):
    pass


class DevConfig(object):
    DEBUG = True
    SECRET_KEY = 'nosecret'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'
