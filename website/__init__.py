'''
This module contains the initialization logic for the flask application
'''
from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

import os

from flask import Flask
from website.const import SHOW_CATAGORIES, MOVIE_CATAGORIES
from website.rss_client import RSSClient

rss_client = RSSClient()
DOMAINS = {'shows': SHOW_CATAGORIES,
           'movies': MOVIE_CATAGORIES}

from website.core import bp as cores_bp
from website.errors import bp as errors_bp


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev'
    )
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.logger.info('Registering blueprint %s', cores_bp.name)
    app.register_blueprint(cores_bp)
    app.logger.info('Registering blueprint %s', errors_bp.name)
    app.register_blueprint(errors_bp)

    return app
