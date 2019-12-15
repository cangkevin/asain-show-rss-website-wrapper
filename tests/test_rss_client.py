from pathlib import Path

import pytest
import requests
import responses

from website.const import (
    MOVIES_RESP_FILE, SHOWS_RESP_FILE, EPISODES_RESP_FILE,
    SOURCES_RESP_FILE, EMPTY_RESP_FILE
)
from website import rss_client


def test_get_movies(mocked_response):
    with open(Path(MOVIES_RESP_FILE), 'rb') as resp:
        mocked_response.add(
            responses.GET, rss_client.build_movies_uri('hk-movies', '1'),
            body=resp, status=200)
        rss_resp = rss_client.get_movies('hk-movies', '1')

        assert rss_resp.title == 'HK Movies'
        assert len(rss_resp.items) == 30
        assert rss_resp.paginations


def test_get_shows(mocked_response):
    with open(Path(SHOWS_RESP_FILE), 'rb') as resp:
        mocked_response.add(
            responses.GET, rss_client.build_shows_uri('hk-drama', '1'),
            body=resp, status=200)
        rss_resp = rss_client.get_shows('hk-drama', '1')

        assert rss_resp.title == 'HK Drama'
        assert len(rss_resp.items) == 30
        assert rss_resp.paginations


def test_get_episodes(mocked_response):
    with open(Path(EPISODES_RESP_FILE), 'rb') as resp:
        mocked_response.add(
            responses.GET, rss_client.build_episodes_uri('12345', '1'),
            body=resp, status=200)
        rss_resp = rss_client.get_episodes('12345', '1')

        assert rss_resp.title == 'The Learning Curve of a Warlord - 大帥哥'
        assert len(rss_resp.items) == 41
        assert not rss_resp.paginations


def test_get_sources(mocked_response):
    with open(Path(SOURCES_RESP_FILE), 'rb') as resp:
        mocked_response.add(
            responses.GET, rss_client.build_sources_uri('99999'),
            body=resp, status=200)
        rss_resp = rss_client.get_sources('99999')

        assert rss_resp.title == 'Episode 22'
        assert len(rss_resp.items) == 2
        assert not rss_resp.paginations


def test_get_movies_timed_out(mocked_response):
    mocked_response.add(
        responses.GET, rss_client.build_movies_uri('hk-movies', '1'),
        body=requests.exceptions.Timeout('')
    )

    with pytest.raises(rss_client.ClientTimeoutError):
        rss_client.get_movies('hk-movies', '1')


def test_get_shows_timed_out(mocked_response):
    mocked_response.add(
        responses.GET, rss_client.build_shows_uri('hk-drama', '1'),
        body=requests.exceptions.Timeout('')
    )

    with pytest.raises(rss_client.ClientTimeoutError):
        rss_client.get_shows('hk-drama', '1')


def test_get_episodes_timed_out(mocked_response):
    mocked_response.add(
        responses.GET, rss_client.build_episodes_uri('12345', '1'),
        body=requests.exceptions.Timeout('')
    )

    with pytest.raises(rss_client.ClientTimeoutError):
        rss_client.get_episodes('12345', '1')


def test_get_sources_timed_out(mocked_response):
    mocked_response.add(
        responses.GET, rss_client.build_sources_uri('99999'),
        body=requests.exceptions.Timeout('')
    )

    with pytest.raises(rss_client.ClientTimeoutError):
        rss_client.get_sources('99999')


def test_get_invalid_movie(mocked_response):
    with open(Path(EMPTY_RESP_FILE), 'rb') as resp:
        mocked_response.add(
            responses.GET, rss_client.build_movies_uri('invalid-movie', '1'),
            body=resp, status=200
        )

        with pytest.raises(rss_client.InvalidResourceError):
            rss_client.get_movies('invalid-movie', '1')


def test_get_invalid_show(mocked_response):
    with open(Path(EMPTY_RESP_FILE), 'rb') as resp:
        mocked_response.add(
            responses.GET, rss_client.build_shows_uri('invalid-show', '1'),
            body=resp, status=200
        )

        with pytest.raises(rss_client.InvalidResourceError):
            rss_client.get_shows('invalid-show', '1')


def test_get_invalid_episode(mocked_response):
    with open(Path(EMPTY_RESP_FILE), 'rb') as resp:
        mocked_response.add(
            responses.GET, rss_client.build_episodes_uri('invalid-ep', '1'),
            body=resp, status=200
        )

        with pytest.raises(rss_client.InvalidResourceError):
            rss_client.get_episodes('invalid-ep', '1')


def test_get_invalid_sources(mocked_response):
    with open(Path(EMPTY_RESP_FILE), 'rb') as resp:
        mocked_response.add(
            responses.GET, rss_client.build_sources_uri('invalid-source'),
            body=resp, status=200
        )

        with pytest.raises(rss_client.InvalidResourceError):
            rss_client.get_sources('invalid-source')


def test_get_invalid_movie_with_5xx(mocked_response):
    with open(Path(EMPTY_RESP_FILE), 'rb') as resp:
        mocked_response.add(
            responses.GET, rss_client.build_movies_uri('invalid-movie', '1'),
            body=resp, status=500
        )

        with pytest.raises(rss_client.ClientTimeoutError):
            rss_client.get_movies('invalid-movie', '1')


def test_get_invalid_show_with_5xx(mocked_response):
    with open(Path(EMPTY_RESP_FILE), 'rb') as resp:
        mocked_response.add(
            responses.GET, rss_client.build_shows_uri('invalid-show', '1'),
            body=resp, status=500
        )

        with pytest.raises(rss_client.ClientTimeoutError):
            rss_client.get_shows('invalid-show', '1')


def test_get_invalid_episode_with_5xx(mocked_response):
    with open(Path(EMPTY_RESP_FILE), 'rb') as resp:
        mocked_response.add(
            responses.GET, rss_client.build_episodes_uri('invalid-ep', '1'),
            body=resp, status=500
        )

        with pytest.raises(rss_client.ClientTimeoutError):
            rss_client.get_episodes('invalid-ep', '1')


def test_get_invalid_sources_with_5xx(mocked_response):
    with open(Path(EMPTY_RESP_FILE), 'rb') as resp:
        mocked_response.add(
            responses.GET, rss_client.build_sources_uri('invalid-source'),
            body=resp, status=500
        )

        with pytest.raises(rss_client.ClientTimeoutError):
            rss_client.get_sources('invalid-source')
