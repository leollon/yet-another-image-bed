import os
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
        'db': 'imgbed4yourself',
        'host': 'mongo',
        'port': 27017,
        'username': 'your_username',
        'password': 'your_password',
        'connect': False
    }


config = {
    'local': DevelopmentConfig,
}
