import functools
import requests
from xml.etree import ElementTree

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('listing', __name__)

@bp.route('/')
def index():
    # TODO: need to optimize from this current setup of two consecutive calls
    #       to improve page loading time;
    #       - check if the URL corresponding to the recently updated listing feed
    #       stays constant; may be able to utilize an async requests library
    r = requests.get('http://rsscity.co/dramacity')

    # get initial RSS feed
    root = ElementTree.fromstring(r.content)
    category_items = [item for item in root.iter('item')]

    # get recently updated listing feed
    recently_updated_catagory = category_items[0]
    recently_updated_catagory_url = recently_updated_catagory.find('enclosure').attrib['url']
    r = requests.get(recently_updated_catagory_url)
    root = ElementTree.fromstring(r.content)

    # get show listings in the recently updated listing feed
    show_listings = [{'title': item.find('title').text, 
                        'url': item.find('enclosure').attrib['url'],
                        'picture': item.find('description').text.strip()} 
                        for item in root.iter('item')]
    
    return render_template('listing/index.html', shows=show_listings)