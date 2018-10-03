import os

DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = os.getenv("USERNAME") or "root"
PASSWORD = os.getenv("PASSWORD") or "ilovemuxi"
HOST = os.getenv("DBHOST") or "localhost"
PORT = os.getenv("DBPORT") or "3306"
DATABASE = "shconnection"


class Config(object):
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = os.getenv("SECRET_KEY") or 'a string hard to guess'
    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = \
        "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(
            DIALECT,
            DRIVER,
            USERNAME,
            PASSWORD,
            HOST,
            PORT,
            DATABASE
        )

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = \
        "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(
            DIALECT,
            DRIVER,
            USERNAME,
            PASSWORD,
            HOST,
            PORT,
            DATABASE
        )


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = \
        "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(
            DIALECT,
            DRIVER,
            USERNAME,
            PASSWORD,
            HOST,
            PORT,
            DATABASE
        )

config = {
    'developments': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
