from urllib.parse import urlparse
from pathlib import Path

import responses

from website import create_app


def test_landing_page_should_redirect(client):
    response = client.get('/')
    assert response.status_code == 302
    assert urlparse(response.location).path == '/shows/recently-added-can-dub/1'


def test_get_movies_page(client, rss_client, mocked_response):
    with open(Path('tests/data/movie_response.txt'), 'rb') as resp:
        mocked_response.add(
            responses.GET, rss_client.build_movies_uri('hk-movies', '1'),
            body=resp, status=200)
        response = client.get('/movies/hk-movies/1')

        assert response.data
        assert response.status_code == 200
        assert len(mocked_response.calls) == 1


def test_get_shows_page(client, rss_client, mocked_response):
    with open(Path('tests/data/show_response.txt'), 'rb') as resp:
        mocked_response.add(
            responses.GET, rss_client.build_shows_uri('hk-drama', '1'),
            body=resp, status=200)
        response = client.get('/shows/hk-drama/1')

        assert response.data
        assert response.status_code == 200
        assert len(mocked_response.calls) == 1


def test_get_episodes_page(client, rss_client, mocked_response):
    with open(Path('tests/data/episode_response.txt'), 'rb') as resp:
        mocked_response.add(
            responses.GET, rss_client.build_episodes_uri('12345', '1'),
            body=resp, status=200)
        response = client.get('/episodes/12345/1')

        assert response.data
        assert response.status_code == 200
        assert len(mocked_response.calls) == 1


def test_get_sources_page(client, rss_client, mocked_response):
    with open(Path('tests/data/sources_response.txt'), 'rb') as resp:
        mocked_response.add(
            responses.GET, rss_client.build_sources_uri('99999'),
            body=resp, status=200)
        response = client.get('/sources/99999')

        assert response.data
        assert response.status_code == 200
        assert len(mocked_response.calls) == 1
