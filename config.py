class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'sqlite:///:memory:'


class ProductionConfig(Config):
    DATABASE_URI = 'mysql://user@localhost/foo'
    DEBUG = True


class DevelopmentConfig(Config):
    DEBUG = True
    LOG_FILE = 'app.log'
    LOG_FORMAT = '%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s'

    # '%(name)s - %(levelname)s - %(message)s'


class TestingConfig(Config):
    TESTING = True
