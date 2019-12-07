from os import environ
from pathlib import Path


class Config(object):
    SECRET_KEY = environ.get("SECRET_KEY")
    UPLOAD_BASE_FOLDER = (Path('/upload').as_posix())  # get absolut path
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # file uploaded max size
    MONGODB_SETTINGS = {
        'db': environ.get("MONGO_INITDB_DATABASE"),
        'host': environ.get("MONGO_HOST"),
        'port': int(environ.get("MONGO_PORT")),
        'username': environ.get("MONGO_USER"),
        'password': environ.get("MONGO_USER_PASSWORD"),
        'connect': False
    }

    @staticmethod
    def init_app(app):
        pass


class TestConfig(Config):
    DEBUG = False
    TESTING = True
    ENV = 'TEST'


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = True
    ENV = 'Develoment'


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    ENV = 'Production'


config = {
    'local': DevelopmentConfig,
    'test': TestConfig,
    'prod': ProductionConfig
}
