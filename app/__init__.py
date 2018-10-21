"""Make directory app as a package
"""
from flask import Flask
from config import config
from flask_wtf.csrf import CSRFProtect
from flask_mongoengine import MongoEngine
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

from app.image.errors import file_too_large

csrf = CSRFProtect()
db = MongoEngine()


def create_app(config_name):
    """Factory of Creating app
    @param:
        config_name - all configurations of app
    """
    sentry_sdk.init(
        dsn="",
        integrations=[FlaskIntegration()])
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    csrf.init_app(app)
    db.init_app(app)

    from .image import image as image_blueprint
    app.register_blueprint(image_blueprint)

    return app
