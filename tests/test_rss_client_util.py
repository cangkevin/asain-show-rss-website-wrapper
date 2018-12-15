import os

from pathlib import Path

import feedparser
from website.rss_client import RSSClientUtil


def test_extract_paginations_with_one_present():
    with open(Path('tests/data/movie_response.txt'), 'rb') as data:
        rss_data = feedparser.parse(data)
        entries = RSSClientUtil.extract_show_or_movie_entries(rss_data)
        paginations = RSSClientUtil.extract_paginations(entries)[1]

        assert paginations


def test_extract_paginations_with_none_present():
    with open(Path('tests/data/episode_response.txt'), 'rb') as data:
        rss_data = feedparser.parse(data)
        entries = RSSClientUtil.extract_episodes(rss_data)
        paginations = RSSClientUtil.extract_paginations(entries)[1]

        assert not paginations


def test_extract_show_or_movie_entries():
    with open(Path('tests/data/movie_response.txt'), 'rb') as data:
        rss_data = feedparser.parse(data)
        entries = RSSClientUtil.extract_show_or_movie_entries(rss_data)

        assert entries


def test_extract_episodes():
    with open(Path('tests/data/episode_response.txt'), 'rb') as data:
        rss_data = feedparser.parse(data)
        entries = RSSClientUtil.extract_episodes(rss_data)
        episodes = RSSClientUtil.extract_paginations(entries)[0]

        assert episodes


def test_extract_picture():
    with open(Path('tests/data/movie_response.txt'), 'rb') as data:
        rss_data = feedparser.parse(data)
        test_entry = rss_data.entries[0]
        picture_url = RSSClientUtil.extract_picture(test_entry)

        assert isinstance(picture_url, str)
        assert '.jpg' in picture_url


def test_extract_id():
    with open(Path('tests/data/movie_response.txt'), 'rb') as data:
        rss_data = feedparser.parse(data)
        test_entry = rss_data.entries[0]
        entry_id = RSSClientUtil.extract_id(test_entry)

        assert entry_id.isnumeric()


def test_extract_sources():
    with open(Path('tests/data/sources_response.txt'), 'rb') as data:
        rss_data = feedparser.parse(data)
        entries = RSSClientUtil.extract_sources(rss_data)

        assert entries
