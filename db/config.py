class Config(object):
    DEBUG = False
    TESTING = False
    PORT = 5000
    DATABASE_URI = 'db/svm.db'
    DATABASE_SCHEMA = 'db/schema.sql'

class ProductionConfig(Config):
    DATABASE_URI = 'mysql://user@localhost/foo'

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
