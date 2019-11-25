"""Make directory app as a package
"""
import sentry_sdk
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from sentry_sdk.integrations.flask import FlaskIntegration

from config import config


def create_app(config_name):
    """Factory of Creating app
    @param:
        config_name - all configurations of app
    """
    sentry_sdk.init(
        dsn="",
        integrations=[FlaskIntegration()])
    application = Flask(__name__)
    application.config.from_object(config[config_name])
    config[config_name].init_app(application)

    csrf = CSRFProtect()

    from .image.model import image_db
    from .image.views import image as image_blueprint
    from .image.apis import blueprint as image_api_blueprint

    csrf.init_app(application)
    image_db.init_app(application)
    application.register_blueprint(image_blueprint)
    application.register_blueprint(image_api_blueprint)

    return application
