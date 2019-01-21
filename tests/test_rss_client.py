from pathlib import Path

import responses
from website import const


def test_get_movies(rss_client, mocked_response):
    with open(Path(const.MOVIES_RESP_FILE), 'rb') as resp:
        mocked_response.add(
            responses.GET, rss_client.build_movies_uri('hk-movies', '1'),
            body=resp, status=200)
        rss_resp = rss_client.get_movies('hk-movies', '1')

        assert rss_resp.title() == 'HK Movies'
        assert len(rss_resp.items()) == 30
        assert rss_resp.paginations()


def test_get_shows(rss_client, mocked_response):
    with open(Path(const.SHOWS_RESP_FILE), 'rb') as resp:
        mocked_response.add(
            responses.GET, rss_client.build_shows_uri('hk-drama', '1'),
            body=resp, status=200)
        rss_resp = rss_client.get_shows('hk-drama', '1')

        assert rss_resp.title() == 'HK Dramas'
        assert len(rss_resp.items()) == 30
        assert rss_resp.paginations()


def test_get_episodes(rss_client, mocked_response):
    with open(Path(const.EPISODES_RESP_FILE), 'rb') as resp:
        mocked_response.add(
            responses.GET, rss_client.build_episodes_uri('12345', '1'),
            body=resp, status=200)
        rss_resp = rss_client.get_episodes('12345', '1')

        assert rss_resp.title() == 'The Learning Curve of a Warlord - 大帥哥'
        assert len(rss_resp.items()) == 41
        assert not rss_resp.paginations()


def test_get_sources(rss_client, mocked_response):
    with open(Path(const.SOURCES_RESP_FILE), 'rb') as resp:
        mocked_response.add(
            responses.GET, rss_client.build_sources_uri('99999'),
            body=resp, status=200)
        rss_resp = rss_client.get_sources('99999')

        assert rss_resp.title() == 'Episode 22'
        assert len(rss_resp.items()) == 3
        assert not rss_resp.paginations()


def test_lookup_page_title(rss_client):
    lookup_valid_category = rss_client.lookup_page_title(
        rss_client.show_categories, 'hk-drama', 'HK Shows'
    )
    lookup_invalid_category = rss_client.lookup_page_title(
        rss_client.movie_categories, 'hk-drama', 'HK Movies'
    )

    assert lookup_valid_category == 'HK Dramas'
    assert lookup_invalid_category == 'HK Movies'
