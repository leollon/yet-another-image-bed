from os import environ
from pathlib import Path


class Config(object):
    SECRET_KEY = 'your_secret_key'
    UPLOAD_BASE_FOLDER = (
        Path.home() / 'upload').as_posix()  # get absolut path
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # file uploaded max size

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = True
    ENV = 'Develoment'
    MONGODB_SETTINGS = {
        'db': environ.get("MONGO_INITDB_DATABASE"),
        'host': environ.get("MONGO_HOST"),
        'port': int(environ.get("MONGO_PORT")),
        'username': environ.get("MONGO_USER"),
        'password': environ.get("MONGO_USER_PASSWORD"),
        'connect': False
    }


config = {
    'local': DevelopmentConfig,
}
