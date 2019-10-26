from .rss_client import RSSClient
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, Flask
)
from . import const

client = RSSClient()
bp = Blueprint('core', __name__)


@bp.route('/')
def index():
    return redirect(url_for('.shows',
                            category='recently-added-can-dub',
                            page=1))


@bp.route('/movies/<category>/<page>')
def movies(category, page):
    response = client.get_movies(category, page)

    return render_template(const.MOVIES_TEMPLATE,
                           domains={'shows': client.show_categories,
                                    'movies': client.movie_categories},
                           current_category=category,
                           response=response)


@bp.route('/shows/<category>/<page>')
def shows(category, page):
    response = client.get_shows(category, page)

    return render_template(const.SHOWS_TEMPLATE,
                           domains={'shows': client.show_categories,
                                    'movies': client.movie_categories},
                           current_category=category,
                           response=response)


@bp.route('/episodes/<show_id>/<page>')
def episodes(show_id, page):
    response = client.get_episodes(show_id, page)

    return render_template(const.EPISODES_TEMPLATE,
                           domains={'shows': client.show_categories,
                                    'movies': client.movie_categories},
                           current_show=show_id,
                           response=response)


@bp.route('/sources/<episode_id>')
def sources(episode_id):
    response = client.get_sources(episode_id)

    return render_template(const.SOURCES_TEMPLATE,
                           domains={'shows': client.show_categories,
                                    'movies': client.movie_categories},
                           response=response)
