import os
import re

from bs4 import BeautifulSoup
from urllib.parse import urlsplit
from more_itertools import unique_everseen


def build_movies_uri(category, page):
    '''Constructs the request URI for movies endpoint'''
    return ''.join([os.getenv('BASE_URL'), 'movies/', category, '/', page])


def build_shows_uri(category, page):
    '''Constructs the request URI for shows endpoint'''
    return ''.join([os.getenv('BASE_URL'), 'category/', category, '/', page])


def build_episodes_uri(show, page):
    '''Constructs the request URI for episodes endpoint'''
    return ''.join([os.getenv('BASE_URL'), 'info/', show, '/', page])


def build_sources_uri(episode):
    '''Constructs the sources URI for sources endpoint'''
    return ''.join([os.getenv('BASE_URL'), 'episode/', episode])


def extract_paginations(entries):
    pagination_pattern = r'Page \d'

    pagination_links = [entry for entry in entries
                        if re.match(pagination_pattern, entry['title'])]
    entries[:] = [entry for entry in entries
                  if not re.match(pagination_pattern, entry['title'])]

    return entries, pagination_links[::-1]


def extract_picture(entry):
    return BeautifulSoup(
        entry.summary,
        features='html.parser').find('img')['src']


def extract_id(entry):
    return os.path.normpath(
        urlsplit(
            entry.links[0].href
        ).path
    ).split(os.sep).pop()


def extract_show_or_movie_entries(data):
    return [{'title': entry.title,
             'picture': extract_picture(entry),
             'id': extract_id(entry)}
            for entry in data.entries]


def extract_episodes(data):
    return [{'title': entry.title,
             'id': extract_id(entry)}
            for entry in data.entries]


def extract_sources(data):
    sources = [{'title': entry.title,
                'url': entry.links[0].href}
               for entry in data.entries]

    return sorted(
        list(
            unique_everseen(
                sources,
                key=lambda e: '{url}'.format(**e))
        ), key=lambda e: e['title'])
