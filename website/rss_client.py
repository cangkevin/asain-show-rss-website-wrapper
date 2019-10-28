import os
import re

from urllib.parse import urlsplit

import requests
import feedparser
import logging

from bs4 import BeautifulSoup
from .models import RSSResponse
from . import const

logger = logging.getLogger(__name__)


class ClientTimeoutError(Exception):
    pass


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
        self.show_categories = const.SHOW_CATAGORIES
        self.movie_categories = const.MOVIE_CATAGORIES

    def lookup_page_title(self, domain, category, resp_page_title):
        for subcategory in domain.values():
            if category in subcategory:
                return subcategory[category]
        return resp_page_title

    def build_movies_uri(self, category, page):
        return ''.join([self.base_url, 'movies/', category, '/', page])

    def build_shows_uri(self, category, page):
        return ''.join([self.base_url, 'category/', category, '/', page])

    def build_episodes_uri(self, show, page):
        return ''.join([self.base_url, 'info/', show, '/', page])

    def build_sources_uri(self, episode):
        return ''.join([self.base_url, 'episode/', episode])

    def get_movies(self, category, page):
        logger.info('Fetching movies for %s, page %s', category, page)
        try:
            response = requests.get(
                self.build_movies_uri(category, page),
                timeout=(6.05, 9)
            )
            rss_data = feedparser.parse(response.content)

            page_title = rss_data.feed.title
            entries = RSSClientUtil.extract_show_or_movie_entries(rss_data)
            episodes, paginations = RSSClientUtil.extract_paginations(entries)

            return RSSResponse(page_title, episodes, paginations)
        except requests.exceptions.Timeout:
            logger.error(
                'Request timed out fetching movies for %s, page %s',
                category, page)
            raise ClientTimeoutError('Timeout fetching movies')

    def get_shows(self, category, page):
        logger.info('Fetching shows for %s, page %s', category, page)
        try:
            response = requests.get(
                self.build_shows_uri(category, page),
                timeout=(6.05, 9)
            )
            rss_data = feedparser.parse(response.content)

            page_title = rss_data.feed.title
            entries = RSSClientUtil.extract_show_or_movie_entries(rss_data)
            episodes, paginations = RSSClientUtil.extract_paginations(entries)

            return RSSResponse(page_title, episodes, paginations)
        except requests.exceptions.Timeout:
            logger.error(
                'Request timed out fetching shows for %s, page %s',
                category, page)
            raise ClientTimeoutError('Timeout fetching shows')

    def get_episodes(self, show, page):
        logger.info('Fetching episodes for %s, page %s', show, page)
        try:
            response = requests.get(
                self.build_episodes_uri(show, page),
                timeout=(6.05, 9)
            )
            rss_data = feedparser.parse(response.content)

            page_title = rss_data.feed.title
            entries = RSSClientUtil.extract_episodes(rss_data)
            episodes, paginations = RSSClientUtil.extract_paginations(entries)

            return RSSResponse(page_title, episodes, paginations)
        except requests.exceptions.Timeout:
            logger.error(
                'Request timed out fetching episodes for %s, page %s',
                show, page)
            raise ClientTimeoutError('Timeout fetching episodes')

    def get_sources(self, episode):
        logger.info('Fetching sources for episode %s', episode)
        try:
            response = requests.get(
                self.build_sources_uri(episode),
                timeout=(6.05, 9)
            )
            rss_data = feedparser.parse(response.content)
            page_title = rss_data.feed.title
            entries = RSSClientUtil.extract_sources(rss_data)

            return RSSResponse(page_title, entries)
        except requests.exceptions.Timeout:
            logger.error(
                'Request timed out fetching sources for episode %s', episode)
            raise ClientTimeoutError('Timeout fetching sources')
