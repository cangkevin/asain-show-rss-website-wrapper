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

from flask import Flask
from elasticsearch import Elasticsearch

from config import Config
from website.core import bp as core_bp
from website.errors import bp as errors_bp
from website.search import bp as search_bp

def create_app(config_object=Config):
    app = Flask(__name__)
    app.config.from_object(config_object)
    app.logger.info('Registering blueprint %s', core_bp.name)
    app.register_blueprint(core_bp)
    app.logger.info('Registering blueprint %s', errors_bp.name)
    app.register_blueprint(errors_bp)
    app.logger.info('Registering blueprint %s', search_bp.name)
    app.register_blueprint(search_bp)
    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
        if 'ELASTICSEARCH_URL' in app.config else None
    return app
