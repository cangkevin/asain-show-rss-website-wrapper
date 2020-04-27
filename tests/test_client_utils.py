import feedparser

from pathlib import Path

from website.client import utils
from website.const import MOVIES_RESP_FILE, EPISODES_RESP_FILE, SOURCES_RESP_FILE


def test_extract_paginations_with_one_present():
    with open(Path(MOVIES_RESP_FILE), "rb") as data:
        rss_data = feedparser.parse(data)
        entries = utils.extract_show_or_movie_entries(rss_data)
        paginations = utils.extract_paginations(entries)[1]

        assert paginations


def test_extract_paginations_with_none_present():
    with open(Path(SOURCES_RESP_FILE), "rb") as data:
        rss_data = feedparser.parse(data)
        entries = utils.extract_episodes(rss_data)
        paginations = utils.extract_paginations(entries)[1]

        assert not paginations


def test_extract_show_or_movie_entries():
    with open(Path(MOVIES_RESP_FILE), "rb") as data:
        rss_data = feedparser.parse(data)
        entries = utils.extract_show_or_movie_entries(rss_data)

        assert entries


def test_extract_episodes():
    with open(Path(EPISODES_RESP_FILE), "rb") as data:
        rss_data = feedparser.parse(data)
        entries = utils.extract_episodes(rss_data)
        episodes = utils.extract_paginations(entries)[0]

        assert episodes


def test_extract_picture():
    with open(Path(MOVIES_RESP_FILE), "rb") as data:
        rss_data = feedparser.parse(data)
        test_entry = rss_data.entries[0]
        picture_url = utils.extract_picture(test_entry)

        assert isinstance(picture_url, str)
        assert ".jpg" in picture_url


def test_extract_id():
    with open(Path(MOVIES_RESP_FILE), "rb") as data:
        rss_data = feedparser.parse(data)
        test_entry = rss_data.entries[0]
        entry_id = utils.extract_id(test_entry)

        assert entry_id.isnumeric()


def test_extract_sources():
    with open(Path(SOURCES_RESP_FILE), "rb") as data:
        rss_data = feedparser.parse(data)
        entries = utils.extract_sources(rss_data)

        assert entries
