'''
This module contains the core functionality of the application.
'''
from flask import render_template
from .rss_client import RSSClient, ClientTimeoutError, InvalidResourceError
from . import const

CLIENT = RSSClient()
DOMAINS = {'shows': CLIENT.show_categories,
           'movies': CLIENT.movie_categories}


def handle_exceptions(func):
    '''Decorator to provide common error handling'''
    def exception_handler(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ClientTimeoutError:
            return render_template(
                const.SERVER_ERROR_TEMPLATE, domains=DOMAINS), 500
        except InvalidResourceError:
            return render_template(
                const.USER_ERROR_TEMPLATE, domains=DOMAINS), 404
    return exception_handler


@handle_exceptions
def get_movies(category, page):
    '''Constructs response for movies in category'''
    response = CLIENT.get_movies(category, page)
    return render_template(
        const.MOVIES_TEMPLATE,
        domains=DOMAINS,
        current_category=category,
        response=response)


@handle_exceptions
def get_shows(category, page):
    '''Constructs response for shows in category'''
    response = CLIENT.get_shows(category, page)
    return render_template(
        const.SHOWS_TEMPLATE,
        domains=DOMAINS,
        current_category=category,
        response=response)


@handle_exceptions
def get_episodes(show, page):
    '''Constructs response for episodes of a show'''
    response = CLIENT.get_episodes(show, page)
    return render_template(
        const.EPISODES_TEMPLATE,
        domains=DOMAINS,
        current_show=show,
        response=response)


@handle_exceptions
def get_sources(episode):
    '''Constructs response for sources of an episode'''
    response = CLIENT.get_sources(episode)
    return render_template(
        const.SOURCES_TEMPLATE,
        domains=DOMAINS,
        response=response)
