'''
This module contains the API interface of the application.
'''
from functools import wraps
from flask import redirect, render_template, url_for
from htmlmin.main import minify

from website import client
from website.core import bp
from website.const import (
    DOMAINS, LISTINGS_TEMPLATE, EPISODES_TEMPLATE, SOURCES_TEMPLATE
)


def templated(template, http_code=200):
    '''Decorator for routes to pass template and HTTP code'''
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            ctx = func(*args, **kwargs)
            return render_template(template, **ctx), http_code
        return decorated_function
    return decorator


@bp.after_request
def minify_response(response):
    '''Minify html response'''
    response.set_data(minify(response.get_data(as_text=True)))
    return response


@bp.app_context_processor
def domains():
    return dict(domains=DOMAINS)


@bp.route('/')
def index():
    '''Endpoint that redirects to a default landing location'''
    return redirect(url_for('.shows',
                            category='recently-added-can-dub',
                            page=1))


@bp.route('/movies/<category>/<page>')
@templated(LISTINGS_TEMPLATE)
def movies(category, page):
    '''Endpoint that returns movies for a given category'''
    return dict(
        current_category=category,
        response=client.get_movies(category, page))


@bp.route('/shows/<category>/<page>')
@templated(LISTINGS_TEMPLATE)
def shows(category, page):
    '''Endpoint that returns shows for a given category'''
    return dict(
        current_category=category,
        response=client.get_shows(category, page))


@bp.route('/episodes/<show_id>/<page>')
@templated(EPISODES_TEMPLATE)
def episodes(show_id, page):
    '''Endpoint that returns episodes for a show id'''
    return dict(
        current_show=show_id,
        response=client.get_episodes(show_id, page))


@bp.route('/sources/<episode_id>')
@templated(SOURCES_TEMPLATE)
def sources(episode_id):
    '''Endpoint that returns sources for an episode id'''
    return dict(response=client.get_sources(episode_id))
