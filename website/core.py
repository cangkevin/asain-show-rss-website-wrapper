'''
This module contains the core functionality of the application.
'''
from .rss_client import RSSClient

CLIENT = RSSClient()
DOMAINS = {'shows': CLIENT.show_categories,
           'movies': CLIENT.movie_categories}


def get_movies(category, page):
    '''Constructs response for movies in category'''
    return CLIENT.get_movies(category, page)


def get_shows(category, page):
    '''Constructs response for shows in category'''
    return CLIENT.get_shows(category, page)


def get_episodes(show, page):
    '''Constructs response for episodes of a show'''
    return CLIENT.get_episodes(show, page)


def get_sources(episode):
    '''Constructs response for sources of an episode'''
    return CLIENT.get_sources(episode)
