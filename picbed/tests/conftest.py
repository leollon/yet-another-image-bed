import pytest

from ..app import create_app
from ..config import config


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app(config['test'])
    yield app


@pytest.fixture
def client():
    """A test client for app."""
    return app.test_client()
