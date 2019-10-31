'''
This module contains the core functionality of the application.
'''
from flask import (
    Blueprint, redirect, render_template, url_for
)
from .rss_client import RSSClient, ClientTimeoutError, InvalidResourceError
from . import const

CLIENT = RSSClient()
BP = Blueprint('core', __name__)


@BP.route('/')
def index():
    '''Endpoint that redirects to a default landing location'''
    return redirect(url_for('.shows',
                            category='recently-added-can-dub',
                            page=1))


@BP.route('/movies/<category>/<page>')
def movies(category, page):
    '''Endpoint that returns movies for a given category'''
    try:
        response = CLIENT.get_movies(category, page)
        return render_template(
            const.MOVIES_TEMPLATE,
            domains={'shows': CLIENT.show_categories,
                     'movies': CLIENT.movie_categories},
            current_category=category,
            response=response)
    except ClientTimeoutError:
        return render_template(
            const.SERVER_ERROR_TEMPLATE,
            domains={'shows': CLIENT.show_categories,
                     'movies': CLIENT.movie_categories}), 500
    except InvalidResourceError:
        return render_template(
            const.USER_ERROR_TEMPLATE,
            domains={'shows': CLIENT.show_categories,
                     'movies': CLIENT.movie_categories}), 404


@BP.route('/shows/<category>/<page>')
def shows(category, page):
    '''Endpoint that returns shows for a given category'''
    try:
        response = CLIENT.get_shows(category, page)
        return render_template(
            const.SHOWS_TEMPLATE,
            domains={'shows': CLIENT.show_categories,
                     'movies': CLIENT.movie_categories},
            current_category=category,
            response=response)
    except ClientTimeoutError:
        return render_template(
            const.SERVER_ERROR_TEMPLATE,
            domains={'shows': CLIENT.show_categories,
                     'movies': CLIENT.movie_categories}), 500
    except InvalidResourceError:
        return render_template(
            const.USER_ERROR_TEMPLATE,
            domains={'shows': CLIENT.show_categories,
                     'movies': CLIENT.movie_categories}), 404


@BP.route('/episodes/<show_id>/<page>')
def episodes(show_id, page):
    '''Endpoint that returns episodes for a show id'''
    try:
        response = CLIENT.get_episodes(show_id, page)
        return render_template(
            const.EPISODES_TEMPLATE,
            domains={'shows': CLIENT.show_categories,
                     'movies': CLIENT.movie_categories},
            current_show=show_id,
            response=response)
    except ClientTimeoutError:
        return render_template(
            const.SERVER_ERROR_TEMPLATE,
            domains={'shows': CLIENT.show_categories,
                     'movies': CLIENT.movie_categories}), 500
    except InvalidResourceError:
        return render_template(
            const.USER_ERROR_TEMPLATE,
            domains={'shows': CLIENT.show_categories,
                     'movies': CLIENT.movie_categories}), 404


@BP.route('/sources/<episode_id>')
def sources(episode_id):
    '''Endpoint that returns sources for an episode id'''
    try:
        response = CLIENT.get_sources(episode_id)
        return render_template(
            const.SOURCES_TEMPLATE,
            domains={'shows': CLIENT.show_categories,
                     'movies': CLIENT.movie_categories},
            response=response)
    except ClientTimeoutError:
        return render_template(
            const.SERVER_ERROR_TEMPLATE,
            domains={'shows': CLIENT.show_categories,
                     'movies': CLIENT.movie_categories}), 500
    except InvalidResourceError:
        return render_template(
            const.USER_ERROR_TEMPLATE,
            domains={'shows': CLIENT.show_categories,
                     'movies': CLIENT.movie_categories}), 404
