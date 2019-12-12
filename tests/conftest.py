import pytest
import responses

from website import create_app
from website.rss_client import RSSClient


@pytest.fixture
def app():
    app = create_app({'TESTING': True})
    app.app_context().push()
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def rss_client():
    return RSSClient()


@pytest.fixture
def mocked_response():
    with responses.RequestsMock() as rsps:
        yield rsps
