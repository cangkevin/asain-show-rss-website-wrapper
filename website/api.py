'''
This module contains the API interface of the application.
'''
from functools import wraps
from flask import (
    Blueprint, redirect, render_template, url_for
)
from .rss_client import ClientTimeoutError, InvalidResourceError
from . import core
from . import const

BP = Blueprint('core', __name__)


def templated(template, http_code=200):
    '''Decorator for routes to pass template and HTTP code'''
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            ctx = func(*args, **kwargs)
            if ctx is None:
                ctx = {}
            elif not isinstance(ctx, dict):
                return ctx
            return render_template(template, **ctx), http_code
        return decorated_function
    return decorator


@BP.errorhandler(ClientTimeoutError)
@templated(const.SERVER_ERROR_TEMPLATE, 500)
def handle_timeout_error(error):
    return dict(domains=core.DOMAINS)


@BP.errorhandler(InvalidResourceError)
@templated(const.USER_ERROR_TEMPLATE, 404)
def handle_invalid_resource_error(error):
    return dict(domains=core.DOMAINS)


@BP.route('/')
def index():
    '''Endpoint that redirects to a default landing location'''
    return redirect(url_for('.shows',
                            category='recently-added-can-dub',
                            page=1))


@BP.route('/movies/<category>/<page>')
@templated(const.MOVIES_TEMPLATE)
def movies(category, page):
    '''Endpoint that returns movies for a given category'''
    return dict(
        domains=core.DOMAINS,
        current_category=category,
        response=core.get_movies(category, page))


@BP.route('/shows/<category>/<page>')
@templated(const.SHOWS_TEMPLATE)
def shows(category, page):
    '''Endpoint that returns shows for a given category'''
    return dict(
        domains=core.DOMAINS,
        current_category=category,
        response=core.get_shows(category, page))


@BP.route('/episodes/<show_id>/<page>')
@templated(const.EPISODES_TEMPLATE)
def episodes(show_id, page):
    '''Endpoint that returns episodes for a show id'''
    return dict(
        domains=core.DOMAINS,
        current_show=show_id,
        response=core.get_episodes(show_id, page))


@BP.route('/sources/<episode_id>')
@templated(const.SOURCES_TEMPLATE)
def sources(episode_id):
    '''Endpoint that returns sources for an episode id'''
    return dict(
        domains=core.DOMAINS,
        response=core.get_sources(episode_id))
