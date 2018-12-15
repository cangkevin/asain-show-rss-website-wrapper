import os

from pathlib import Path

import responses


def test_get_movies(rss_client, mocked_response):
    with open(Path('tests/data/movie_response.txt'), 'rb') as resp:
        mocked_response.add(
            responses.GET, ''.join([os.environ.get('BASE_URL'), 'movies/',
                                    'hk-movies', '/', '1']),
            body=resp, status=200)
        rss_resp = rss_client.get_movies('hk-movies', '1')

        assert rss_resp.title() == 'HK Movies'
        assert len(rss_resp.items()) == 30
        assert rss_resp.paginations()


def test_get_shows(rss_client, mocked_response):
    with open(Path('tests/data/show_response.txt'), 'rb') as resp:
        mocked_response.add(
            responses.GET, ''.join([os.environ.get('BASE_URL'), 'category/',
                                    'hk-drama', '/', '1']),
            body=resp, status=200)
        rss_resp = rss_client.get_shows('hk-drama', '1')

        assert rss_resp.title() == 'HK Drama'
        assert len(rss_resp.items()) == 30
        assert rss_resp.paginations()


def test_get_episodes(rss_client, mocked_response):
    with open(Path('tests/data/episode_response.txt'), 'rb') as resp:
        mocked_response.add(
            responses.GET, ''.join([os.environ.get('BASE_URL'), 'info/'
                                    '12345', '/', '1']),
            body=resp, status=200)
        rss_resp = rss_client.get_episodes('12345', '1')

        assert rss_resp.title() == 'The Learning Curve of a Warlord - 大帥哥'
        assert len(rss_resp.items()) == 41
        assert not rss_resp.paginations()


def test_get_sources(rss_client, mocked_response):
    with open(Path('tests/data/sources_response.txt'), 'rb') as resp:
        mocked_response.add(
            responses.GET, ''.join([os.environ.get('BASE_URL'), 'episode/',
                                    '99999']),
            body=resp, status=200)
        rss_resp = rss_client.get_sources('99999')

        assert rss_resp.title() == 'Episode 22'
        assert len(rss_resp.items()) == 3
        assert not rss_resp.paginations()
