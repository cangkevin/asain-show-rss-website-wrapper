'''
This module handles a client that interacts with the backend data source
'''
import os
import re

from urllib.parse import urlsplit

import logging
import requests
import feedparser

from bs4 import BeautifulSoup
from .models import RSSResponse
from . import const

LOGGER = logging.getLogger(__name__)


class ClientTimeoutError(Exception):
    '''Custom exception class for timed out client requests'''


class InvalidResourceError(Exception):
    '''Custom exception class for invalid resources'''


class RSSClientUtil:
    '''Class that assists with parsing responses from the RSS data source'''
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
    '''
    Class that serves as a client to communicate with the backend
    RSS data source
    '''
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
        '''Constructs the request URI for movies endpoint'''
        return ''.join([self.base_url, 'movies/', category, '/', page])

    def build_shows_uri(self, category, page):
        '''Constructs the request URI for shows endpoint'''
        return ''.join([self.base_url, 'category/', category, '/', page])

    def build_episodes_uri(self, show, page):
        '''Constructs the request URI for episodes endpoint'''
        return ''.join([self.base_url, 'info/', show, '/', page])

    def build_sources_uri(self, episode):
        '''Constructs the sources URI for sources endpoint'''
        return ''.join([self.base_url, 'episode/', episode])

    def get_movies(self, category, page):
        '''Gets movies for a category'''
        LOGGER.info('Fetching movies for %s, page %s', category, page)
        try:
            response = requests.get(
                self.build_movies_uri(category, page),
                timeout=(6.05, 9)
            )
            rss_data = feedparser.parse(response.content)

            page_title = rss_data.feed.title
            entries = RSSClientUtil.extract_show_or_movie_entries(rss_data)
            movies, paginations = RSSClientUtil.extract_paginations(entries)

            return RSSResponse(page_title, movies, paginations)
        except requests.exceptions.Timeout:
            LOGGER.error(
                'Request timed out fetching movies for %s, page %s',
                category, page)
            raise ClientTimeoutError('Timeout fetching movies')
        except AttributeError:
            LOGGER.error('No movies found; invalid category: %s', category)
            raise InvalidResourceError('No movies found')

    def get_shows(self, category, page):
        '''Gets shows for a category'''
        LOGGER.info('Fetching shows for %s, page %s', category, page)
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
            LOGGER.error(
                'Request timed out fetching shows for %s, page %s',
                category, page)
            raise ClientTimeoutError('Timeout fetching shows')
        except AttributeError:
            LOGGER.error('No shows found; invalid category: %s', category)
            raise InvalidResourceError('No shows found')

    def get_episodes(self, show, page):
        '''Gets episodes for a show'''
        LOGGER.info('Fetching episodes for %s, page %s', show, page)
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
            LOGGER.error(
                'Request timed out fetching episodes for %s, page %s',
                show, page)
            raise ClientTimeoutError('Timeout fetching episodes')
        except AttributeError:
            LOGGER.error('No episodes found; invalid show: %s', show)
            raise InvalidResourceError('No episodes found')

    def get_sources(self, episode):
        '''Gets sources for an episode'''
        LOGGER.info('Fetching sources for episode %s', episode)
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
            LOGGER.error(
                'Request timed out fetching sources for episode %s', episode)
            raise ClientTimeoutError('Timeout fetching sources')
        except AttributeError:
            LOGGER.error('No sources found; invalid episode: %s', episode)
            raise InvalidResourceError('No sources found')
