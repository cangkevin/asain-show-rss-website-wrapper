import os
import re
import functools
import requests
import feedparser
from bs4 import BeautifulSoup
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

CATEGORIES = {
    'recently-added-can-dub': 'Recently Added (Cantonese)',
    'hk-drama': 'HK Drama',
    'hk-show': 'HK Variety & News',
    'c-drama': 'China Drama (English)',
    'c-drama-can-dub': 'China Drama (Cantonese)'
}
BASE_URL = os.environ.get('BASE_URL')

bp = Blueprint('listing',__name__)

def _is_pagination(title):
    pagination_pattern = r'Page \d'
    return re.match(pagination_pattern, title)

def _extract_possible_paginations(entries):
    pagination_links = [entry for entry in entries if _is_pagination(entry['title'])]
    entries[:] = [entry for entry in entries if not _is_pagination(entry['title'])]
    return entries, pagination_links[::-1]


@bp.route('/')
def index():
    return redirect(url_for('.shows',category='recently-added-can-dub',page=1))


@bp.route('/shows/<category>/<page>')
def shows(category,page):
    response = requests.get(BASE_URL + '/category/' + category + '/' + page)
    rss_data = feedparser.parse(response.content)

    page_title = rss_data.feed.title
    entries = [{'title': entry.title,
                'picture': BeautifulSoup(entry.summary).find('img')['src'],
                'id': os.path.normpath(urlsplit(entry.links[0].href).path).split(os.sep).pop()} 
                for entry in rss_data.entries]
    shows, paginations = _extract_possible_paginations(entries)

    return render_template('listing/shows.html',categories=CATEGORIES,
                                                current_category=category,
                                                page_title=page_title,
                                                shows=shows,
                                                paginations=paginations)

@bp.route('/episodes/<show_id>/<page>')
def episodes(show_id,page):
    response = requests.get(BASE_URL + '/info/' + show_id + '/' + page)
    rss_data = feedparser.parse(response.content)

    page_title = rss_data.feed.title
    entries = [{'title': entry.title,
                'id': os.path.normpath(urlsplit(entry.links[0].href).path).split(os.sep).pop()} 
                for entry in rss_data.entries]
    episodes, paginations = _extract_possible_paginations(entries)

    return render_template('listing/episodes.html',categories=CATEGORIES,
                                                    current_show=show_id,
                                                    page_title=page_title,
                                                    episodes=episodes,
                                                    paginations=paginations)

@bp.route('/sources/<episode_id>')
def sources(episode_id):
    response = requests.get(BASE_URL + '/episode/' + episode_id)
    rss_data = feedparser.parse(response.content)

    page_title = rss_data.feed.title
    entries = [{'title': entry.title,
                'url': entry.links[0].href} 
                for entry in rss_data.entries]

    return render_template('listing/sources.html', categories=CATEGORIES,
                                                    page_title=page_title,
                                                    sources=entries)
