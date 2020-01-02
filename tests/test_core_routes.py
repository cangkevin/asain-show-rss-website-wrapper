from urllib.parse import urlparse
from pathlib import Path

import requests
import responses

from website.client.utils import (
    build_movies_uri, build_shows_uri, build_episodes_uri, build_sources_uri
)
from website.const import (
    MOVIES_RESP_FILE, EPISODES_RESP_FILE,
    SOURCES_RESP_FILE, SHOWS_RESP_FILE, EMPTY_RESP_FILE
)


def test_landing_page_should_redirect(client):
    response = client.get('/')
    assert response.status_code == 302
    assert urlparse(response.location).path == \
        '/shows/recently-added-can-dub/1'


def test_get_movies_page(client, mocked_response):
    with open(Path(MOVIES_RESP_FILE), 'rb') as resp:
        mocked_response.add(
            responses.GET, build_movies_uri('hk-movies', '1'),
            body=resp, status=200)
        response = client.get('/movies/hk-movies/1')

        assert response.data
        assert response.status_code == 200
        assert len(mocked_response.calls) == 1


def test_get_shows_page(client, mocked_response):
    with open(Path(SHOWS_RESP_FILE), 'rb') as resp:
        mocked_response.add(
            responses.GET, build_shows_uri('hk-drama', '1'),
            body=resp, status=200)
        response = client.get('/shows/hk-drama/1')

        assert response.data
        assert response.status_code == 200
        assert len(mocked_response.calls) == 1


def test_get_episodes_page(client, mocked_response):
    with open(Path(EPISODES_RESP_FILE), 'rb') as resp:
        mocked_response.add(
            responses.GET, build_episodes_uri('12345', '1'),
            body=resp, status=200)
        response = client.get('/episodes/12345/1')

        assert response.data
        assert response.status_code == 200
        assert len(mocked_response.calls) == 1


def test_get_sources_page(client, mocked_response):
    with open(Path(SOURCES_RESP_FILE), 'rb') as resp:
        mocked_response.add(
            responses.GET, build_sources_uri('99999'),
            body=resp, status=200)
        response = client.get('/sources/99999')

        assert response.data
        assert response.status_code == 200
        assert len(mocked_response.calls) == 1


def test_get_movies_page_timeout(client, mocked_response):
    mocked_response.add(
        responses.GET, build_movies_uri('hk-movies', '1'),
        body=requests.exceptions.Timeout('')
    )
    response = client.get('/movies/hk-movies/1')

    assert response.data
    assert response.status_code == 500


def test_get_shows_page_timeout(client, mocked_response):
    mocked_response.add(
        responses.GET, build_shows_uri('hk-drama', '1'),
        body=requests.exceptions.Timeout('')
    )
    response = client.get('/shows/hk-drama/1')

    assert response.data
    assert response.status_code == 500


def test_get_episodes_page_timeout(client, mocked_response):
    mocked_response.add(
        responses.GET, build_episodes_uri('12345', '1'),
        body=requests.exceptions.Timeout('')
    )
    response = client.get('/episodes/12345/1')

    assert response.data
    assert response.status_code == 500


def test_get_sources_page_timeout(client, mocked_response):
    mocked_response.add(
        responses.GET, build_sources_uri('999999'),
        body=requests.exceptions.Timeout('')
    )
    response = client.get('/sources/999999')

    assert response.data
    assert response.status_code == 500


def test_get_nonexistent_movies_page(client, mocked_response):
    with open(Path(EMPTY_RESP_FILE), 'rb') as resp:
        mocked_response.add(
            responses.GET,
            build_movies_uri('invalid-category', '1'),
            body=resp, status=200
        )
        response = client.get('/movies/invalid-category/1')

        assert response.data
        assert response.status_code == 404


def test_get_nonexistent_shows_page(client, mocked_response):
    with open(Path(EMPTY_RESP_FILE), 'rb') as resp:
        mocked_response.add(
            responses.GET, build_shows_uri('invalid-category', '1'),
            body=resp, status=200
        )
        response = client.get('/shows/invalid-category/1')

        assert response.data
        assert response.status_code == 404


def test_get_nonexistent_episodes_page(client, mocked_response):
    with open(Path(EMPTY_RESP_FILE), 'rb') as resp:
        mocked_response.add(
            responses.GET, build_episodes_uri('invalid-show', '1'),
            body=resp, status=200
        )
        response = client.get('/episodes/invalid-show/1')

        assert response.data
        assert response.status_code == 404


def test_get_nonexistent_sources_page(client, mocked_response):
    with open(Path(EMPTY_RESP_FILE), 'rb') as resp:
        mocked_response.add(
            responses.GET, build_sources_uri('invalid-ep'),
            body=resp, status=200
        )
        response = client.get('/sources/invalid-ep')

        assert response.data
        assert response.status_code == 404
