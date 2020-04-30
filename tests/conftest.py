import pytest
import responses

from config import TestConfig
from website import create_app


@pytest.fixture(autouse=True)
def mock_base_url(monkeypatch):
    monkeypatch.setenv("BASE_URL", "http://base_url/")


@pytest.fixture
def app():
    app = create_app(TestConfig())
    app.app_context().push()
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def mocked_response():
    with responses.RequestsMock() as rsps:
        yield rsps
