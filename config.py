import os


class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev'
    BASE_URL = os.environ.get('BASE_URL')
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH') \
        or 'http://localhost:9200'


class TestConfig(Config):
    BASE_URL = 'http://base_url/'
    TESTING = True
