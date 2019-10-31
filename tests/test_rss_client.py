from pathlib import Path

import pytest
import requests
import responses

from website import const
from website.rss_client import ClientTimeoutError, InvalidResourceError


def test_get_movies(rss_client, mocked_response):
    with open(Path(const.MOVIES_RESP_FILE), 'rb') as resp:
        mocked_response.add(
            responses.GET, rss_client.build_movies_uri('hk-movies', '1'),
            body=resp, status=200)
        rss_resp = rss_client.get_movies('hk-movies', '1')

        assert rss_resp.title == 'HK Movies'
        assert len(rss_resp.items) == 30
        assert rss_resp.paginations


def test_get_shows(rss_client, mocked_response):
    with open(Path(const.SHOWS_RESP_FILE), 'rb') as resp:
        mocked_response.add(
            responses.GET, rss_client.build_shows_uri('hk-drama', '1'),
            body=resp, status=200)
        rss_resp = rss_client.get_shows('hk-drama', '1')

        assert rss_resp.title == 'HK Drama'
        assert len(rss_resp.items) == 30
        assert rss_resp.paginations


def test_get_episodes(rss_client, mocked_response):
    with open(Path(const.EPISODES_RESP_FILE), 'rb') as resp:
        mocked_response.add(
            responses.GET, rss_client.build_episodes_uri('12345', '1'),
            body=resp, status=200)
        rss_resp = rss_client.get_episodes('12345', '1')

        assert rss_resp.title == 'The Learning Curve of a Warlord - 大帥哥'
        assert len(rss_resp.items) == 41
        assert not rss_resp.paginations


def test_get_sources(rss_client, mocked_response):
    with open(Path(const.SOURCES_RESP_FILE), 'rb') as resp:
        mocked_response.add(
            responses.GET, rss_client.build_sources_uri('99999'),
            body=resp, status=200)
        rss_resp = rss_client.get_sources('99999')

        assert rss_resp.title == 'Episode 22'
        assert len(rss_resp.items) == 3
        assert not rss_resp.paginations


def test_get_movies_timed_out(rss_client, mocked_response):
    mocked_response.add(
        responses.GET, rss_client.build_movies_uri('hk-movies', '1'),
        body=requests.exceptions.Timeout('')
    )

    with pytest.raises(ClientTimeoutError):
        rss_client.get_movies('hk-movies', '1')


def test_get_shows_timed_out(rss_client, mocked_response):
    mocked_response.add(
        responses.GET, rss_client.build_shows_uri('hk-drama', '1'),
        body=requests.exceptions.Timeout('')
    )

    with pytest.raises(ClientTimeoutError):
        rss_client.get_shows('hk-drama', '1')


def test_get_episodes_timed_out(rss_client, mocked_response):
    mocked_response.add(
        responses.GET, rss_client.build_episodes_uri('12345', '1'),
        body=requests.exceptions.Timeout('')
    )

    with pytest.raises(ClientTimeoutError):
        rss_client.get_episodes('12345', '1')


def test_get_sources_timed_out(rss_client, mocked_response):
    mocked_response.add(
        responses.GET, rss_client.build_sources_uri('99999'),
        body=requests.exceptions.Timeout('')
    )

    with pytest.raises(ClientTimeoutError):
        rss_client.get_sources('99999')


def test_get_invalid_movie(rss_client, mocked_response):
    with open(Path(const.EMPTY_RESP_FILE), 'rb') as resp:
        mocked_response.add(
            responses.GET, rss_client.build_movies_uri('invalid-movie', '1'),
            body=resp, status=200
        )

        with pytest.raises(InvalidResourceError):
            rss_client.get_movies('invalid-movie', '1')


def test_get_invalid_show(rss_client, mocked_response):
    with open(Path(const.EMPTY_RESP_FILE), 'rb') as resp:
        mocked_response.add(
            responses.GET, rss_client.build_shows_uri('invalid-show', '1'),
            body=resp, status=200
        )

        with pytest.raises(InvalidResourceError):
            rss_client.get_shows('invalid-show', '1')


def test_get_invalid_episode(rss_client, mocked_response):
    with open(Path(const.EMPTY_RESP_FILE), 'rb') as resp:
        mocked_response.add(
            responses.GET, rss_client.build_episodes_uri('invalid-ep', '1'),
            body=resp, status=200
        )

        with pytest.raises(InvalidResourceError):
            rss_client.get_episodes('invalid-ep', '1')


def test_get_invalid_sources(rss_client, mocked_response):
    with open(Path(const.EMPTY_RESP_FILE), 'rb') as resp:
        mocked_response.add(
            responses.GET, rss_client.build_sources_uri('invalid-source'),
            body=resp, status=200
        )

        with pytest.raises(InvalidResourceError):
            rss_client.get_sources('invalid-source')
