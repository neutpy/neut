import pytest
from fastapi.testclient import TestClient
from neut.core.app import NeutApp
from neut.core.settings import NeutSettings

@pytest.fixture
def test_settings():
    return NeutSettings(
        PROJECT_NAME="Test Project",
        DEBUG=True,
        DATABASE_URL="sqlite:///./test.db",
        INSTALLED_APPS=[],
        MIDDLEWARES=["neut.core.middleware.cors_middleware"]
    )

@pytest.fixture
def test_app(test_settings):
    app = NeutApp()
    app.state.settings = test_settings
    return app

@pytest.fixture
def client(test_app):
    return TestClient(test_app)