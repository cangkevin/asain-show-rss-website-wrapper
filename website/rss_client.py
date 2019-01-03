import os
import re

from urllib.parse import urlsplit

import requests
import feedparser

from bs4 import BeautifulSoup
from .models import RSSResponse


class RSSClientUtil:
    @staticmethod
    def extract_paginations(entries):
        pagination_pattern = r'Page \d'

        pagination_links = [entry for entry in entries
                            if re.match(pagination_pattern, entry['title'])]
        entries[:] = [entry for entry in entries
                      if not re.match(pagination_pattern, entry['title'])]

        return entries, pagination_links[::-1]

    @staticmethod
    def extract_picture(entry):
        return BeautifulSoup(
            entry.summary,
            features='html.parser').find('img')['src']

    @staticmethod
    def extract_id(entry):
        return os.path.normpath(
            urlsplit(
                entry.links[0].href
            ).path
        ).split(os.sep).pop()

    @staticmethod
    def extract_show_or_movie_entries(data):
        return [{'title': entry.title,
                 'picture': RSSClientUtil.extract_picture(entry),
                 'id': RSSClientUtil.extract_id(entry)}
                for entry in data.entries]

    @staticmethod
    def extract_episodes(data):
        return [{'title': entry.title,
                 'id': RSSClientUtil.extract_id(entry)}
                for entry in data.entries]

    @staticmethod
    def extract_sources(data):
        return [{'title': entry.title,
                 'url': entry.links[0].href}
                for entry in data.entries]


class RSSClient:
    def __init__(self):
        self.base_url = os.environ.get('BASE_URL')
        self.show_categories = {
            'recently-added-can-dub': 'Recently Added (Cantonese)',
            'hk-drama': 'HK Drama',
            'hk-show': 'HK Variety & News',
            'c-drama': 'China Drama (English)',
            'c-drama-can-dub': 'China Drama (Cantonese)'
        }
        self.movie_categories = {
            'recently-added-can-dub': 'Recently Added (Cantonese)',
            'hk-movies': 'HK Movies',
            'c-movies-can-dub': 'China Movies (Cantonese)'
        }

    def build_movies_uri(self, category, page):
        return ''.join([self.base_url, 'movies/', category, '/', page])

    def build_shows_uri(self, category, page):
        return ''.join([self.base_url, 'category/', category, '/', page])

    def build_episodes_uri(self, show, page):
        return ''.join([self.base_url, 'info/', show, '/', page])

    def build_sources_uri(self, episode):
        return ''.join([self.base_url, 'episode/', episode])

    def get_movies(self, category, page):
        response = requests.get(self.build_movies_uri(category, page))
        rss_data = feedparser.parse(response.content)

        page_title = rss_data.feed.title
        entries = RSSClientUtil.extract_show_or_movie_entries(rss_data)
        episodes, paginations = RSSClientUtil.extract_paginations(entries)

        return RSSResponse(page_title, episodes, paginations)

    def get_shows(self, category, page):
        response = requests.get(self.build_shows_uri(category, page))
        rss_data = feedparser.parse(response.content)

        page_title = rss_data.feed.title
        entries = RSSClientUtil.extract_show_or_movie_entries(rss_data)
        episodes, paginations = RSSClientUtil.extract_paginations(entries)

        return RSSResponse(page_title, episodes, paginations)

    def get_episodes(self, show, page):
        response = requests.get(self.build_episodes_uri(show, page))
        rss_data = feedparser.parse(response.content)

        page_title = rss_data.feed.title
        entries = RSSClientUtil.extract_episodes(rss_data)
        episodes, paginations = RSSClientUtil.extract_paginations(entries)

        return RSSResponse(page_title, episodes, paginations)

    def get_sources(self, episode):
        response = requests.get(self.build_sources_uri(episode))
        rss_data = feedparser.parse(response.content)
        page_title = rss_data.feed.title
        entries = RSSClientUtil.extract_sources(rss_data)

        return RSSResponse(page_title, entries)
