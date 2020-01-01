import requests
import feedparser
import logging

from website.models import RssResponse
from website.client import utils
from website.client import exceptions

logger = logging.getLogger(__name__)


def handle_exceptions(resource):
    '''Decorator to provide common error handling'''
    def exception_handler_wrapper(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except requests.exceptions.Timeout:
                logger.error(
                    'Request timed out fetching %s for %s', resource, args[0])
                raise exceptions.ClientTimeoutError(
                    'Timeout fetching ' + resource)
            except AttributeError:
                logger.error('No %s found for %s', resource, args[0])
                raise exceptions.InvalidResourceError(resource + ' not found')
        return wrapper
    return exception_handler_wrapper


@handle_exceptions('movies')
def get_movies(category, page):
    '''Gets movies for a category'''
    logger.info('Fetching movies for %s, page %s', category, page)
    response = requests.get(
        utils.build_movies_uri(category, page),
        timeout=(9.05, 9)
    )

    if response.status_code >= 500:
        raise exceptions.ClientTimeoutError('Unable to handle request')

    rss_data = feedparser.parse(response.content)

    page_title = rss_data.feed.title
    entries = utils.extract_show_or_movie_entries(rss_data)
    movies, paginations = utils.extract_paginations(entries)

    return RssResponse(page_title, movies, paginations)


@handle_exceptions('shows')
def get_shows(category, page):
    '''Gets shows for a category'''
    logger.info('Fetching shows for %s, page %s', category, page)
    response = requests.get(
        utils.build_shows_uri(category, page),
        timeout=(9.05, 9)
    )

    if response.status_code >= 500:
        raise exceptions.ClientTimeoutError('Unable to handle request')

    rss_data = feedparser.parse(response.content)

    page_title = rss_data.feed.title
    entries = utils.extract_show_or_movie_entries(rss_data)
    episodes, paginations = utils.extract_paginations(entries)

    return RssResponse(page_title, episodes, paginations)


@handle_exceptions('episodes')
def get_episodes(show, page):
    '''Gets episodes for a show'''
    logger.info('Fetching episodes for %s, page %s', show, page)
    response = requests.get(
        utils.build_episodes_uri(show, page),
        timeout=(9.05, 9)
    )

    if response.status_code >= 500:
        raise exceptions.ClientTimeoutError('Unable to handle request')

    rss_data = feedparser.parse(response.content)

    page_title = rss_data.feed.title
    entries = utils.extract_episodes(rss_data)
    episodes, paginations = utils.extract_paginations(entries)

    return RssResponse(page_title, episodes, paginations)


@handle_exceptions('sources')
def get_sources(episode):
    '''Gets sources for an episode'''
    logger.info('Fetching sources for episode %s', episode)
    response = requests.get(
        utils.build_sources_uri(episode),
        timeout=(9.05, 9)
    )

    if response.status_code >= 500:
        raise exceptions.ClientTimeoutError('Unable to handle request')

    rss_data = feedparser.parse(response.content)
    page_title = rss_data.feed.title
    entries = utils.extract_sources(rss_data)

    return RssResponse(page_title, entries, None)
