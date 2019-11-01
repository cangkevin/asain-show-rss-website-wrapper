'''
This module contains the API interface of the application.
'''
from flask import (
    Blueprint, redirect, url_for
)
from .rss_client import RSSClient
from . import core

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
    return core.get_movies(category, page)


@BP.route('/shows/<category>/<page>')
def shows(category, page):
    '''Endpoint that returns shows for a given category'''
    return core.get_shows(category, page)


@BP.route('/episodes/<show_id>/<page>')
def episodes(show_id, page):
    '''Endpoint that returns episodes for a show id'''
    return core.get_episodes(show_id, page)


@BP.route('/sources/<episode_id>')
def sources(episode_id):
    '''Endpoint that returns sources for an episode id'''
    return core.get_sources(episode_id)
