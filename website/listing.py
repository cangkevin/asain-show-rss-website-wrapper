import functools
import requests
import re

from urllib.parse import urlparse, parse_qs, urlencode
from bs4 import BeautifulSoup
from xml.etree import ElementTree

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('listing', __name__)
_category_endpoints = {
    'recently-updated': 'aHR0cDovL2RyYW1hY2l0eS5pby8=',
    'hk-drama': 'aHR0cDovL2RyYW1hY2l0eS5pby9ob25nLWtvbmctZHJhbWEv',
    'hk-variety-news': 'aHR0cDovL2RyYW1hY2l0eS5pby9ob25nLWtvbmctc2hvdy8=',
    'k-drama': 'aHR0cDovL2RyYW1hY2l0eS5pby9rb3JlYS1kcmFtYS8=',
    'tw-drama': 'aHR0cDovL2RyYW1hY2l0eS5pby90YWl3YW4tZHJhbWEv',
    'c-drama': 'aHR0cDovL2RyYW1hY2l0eS5pby9jaGluZXNlLWRyYW1hLTEv',
    'j-drama': 'aHR0cDovL2RyYW1hY2l0eS5pby9qYXBhbmVzZS1kcmFtYS8=',
    'movies': 'aHR0cDovL2RyYW1hY2l0eS5pby9tb3ZpZXMv'
}
_category_text = {
    'recently-updated': 'Recently Updated',
    'hk-drama': 'HK Drama',
    'hk-variety-news': 'HK Variety/News',
    'k-drama': 'Korean Drama',
    'tw-drama': 'Taiwanese Drama',
    'c-drama': 'Chinese Drama',
    'j-drama': 'Japanese Drama',
    'movies': 'Movies'
}

_ignore_shows = ['aHR0cDovL2RyYW1hY2l0eS5pby9ob3ctdG8td2F0Y2gtZHJhbWEtbW92aWVzLXNob3dzLW9uLW1vYmlsZS1hcHAv']

def _contains_date(text):
    date_pattern = '\d{4}-\d{2}-\d{2}'
    return re.search(date_pattern, text)

def _retrieve_listings(xml_root):
    return [{'title': item.find('title').text,
                'url': parse_qs(urlparse(item.find('enclosure').attrib['url']).query),
                'picture': BeautifulSoup(item.find('description').text.strip()).find('img')['src']}
                 for item in xml_root.iter('item')]

def _retrieve_possible_pagination_link(listing):
    possible_pagination = listing.pop()
    possible_pagination_url = possible_pagination['url']
    if 'page' not in possible_pagination_url:
        listing.append(possible_pagination)
        possible_pagination = None
    return listing, possible_pagination

def _fetch_show_id(url_info):
    if 'film' in url_info.keys():
        show_id = url_info['film'][0]
    elif 'ep' in url_info.keys():
        show_id = url_info['ep'][0]
    return show_id

@bp.route('/')
def index():
    return redirect(url_for('.shows',category='recently-updated',page_num=1))

@bp.route('/<category>/page/<page_num>')
def shows(category,page_num):
    r = requests.get('http://rsscity.co/dramacity/',params={'channel':_category_endpoints[category], 
                                                            'page':page_num})
    root = ElementTree.fromstring(r.content)[0]
    show_listings = _retrieve_listings(root)
    show_listings, possible_pagination = _retrieve_possible_pagination_link(show_listings)
    show_listings = [show for show in show_listings if _fetch_show_id(show['url']) not in _ignore_shows]

    return render_template('listing/shows.html',shows=show_listings,
                                                next_page=possible_pagination,
                                                category=category,
                                                categories_text=_category_text,
                                                contains_date=_contains_date,
                                                ignore_list=_ignore_shows)

@bp.route('/<show_id>/episodes/page/<page_num>')
def episodes(show_id, page_num):
    r = requests.get('http://rsscity.co/dramacity/',params={'film':show_id,
                                                            'page':page_num})
    root = ElementTree.fromstring(r.content)[0]
    episodes = _retrieve_listings(root)
    episodes, possible_pagination = _retrieve_possible_pagination_link(episodes)

    if len(episodes) == 1 and not episodes[0]['url']:
        return redirect(url_for('.sources', episode_id=show_id))

    return render_template('listing/episodes.html',episodes=episodes,
                                                    next_page=possible_pagination,
                                                    categories_text=_category_text)

@bp.route('/<episode_id>/sources')
def sources(episode_id):
    r = requests.get('http://rsscity.co/dramacity/',params={'ep':episode_id})
    
    root = ElementTree.fromstring(r.content)[0]
    title = root.find('title').text
    sources = [{'source': item.find('title').text,
                'url': item.find('enclosure').attrib['url']}
                for item in root.iter('item')]

    return render_template('listing/sources.html',sources=sources,
                                                    title=title,
                                                    categories_text=_category_text)