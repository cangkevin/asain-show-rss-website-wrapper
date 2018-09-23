import requests
import feedparser
import re
import os
from bs4 import BeautifulSoup
from urllib.parse import urlsplit
from .models import RSSResponse

class RSSClientUtil:
    @staticmethod
    def is_pagination(title):
        pagination_pattern = r'Page \d'
        return re.match(pagination_pattern, title)

    @staticmethod
    def extract_possible_paginations(entries):
        pagination_links = [entry for entry in entries if RSSClientUtil.is_pagination(entry['title'])]
        entries[:] = [entry for entry in entries if not RSSClientUtil.is_pagination(entry['title'])]
        return entries, pagination_links[::-1]


class RSSClient:
    def __init__(self):
        self._base_url = 'http://myrss.nu/drama/'
        self.show_categories = {
            'recently-added-can-dub': 'Recently Added (Cantonese)',
            'hk-drama': 'HK Drama',
            'hk-show': 'HK Variety & News',
            'c-drama': 'China Drama (English)',
            'c-drama-can-dub': 'China Drama (Cantonese)'
        }
        self.movie_categories = {
            'recently-added-can-dub': 'Recently Added (Cantonese)',
            'hk-movies': 'HK Movies',
            'c-movies-can-dub': 'China Movies (Cantonese)'
        }

    def get_movies(self, category, page):
        response = requests.get(self._base_url + '/movies/' + category + '/' + page)
        rss_data = feedparser.parse(response.content)

        page_title = rss_data.feed.title
        entries = [{'title': entry.title,
                    'picture': BeautifulSoup(entry.summary,features='html.parser').find('img')['src'],
                    'id': os.path.normpath(urlsplit(entry.links[0].href).path).split(os.sep).pop()}
                    for entry in rss_data.entries]
        episodes, paginations = RSSClientUtil.extract_possible_paginations(entries)

        return RSSResponse(page_title, episodes, paginations)
        
    def get_shows(self, category, page):
        response = requests.get(self._base_url + '/category/' + category + '/' + page)
        rss_data = feedparser.parse(response.content)

        page_title = rss_data.feed.title
        entries = [{'title': entry.title,
                    'picture': BeautifulSoup(entry.summary,features='html.parser').find('img')['src'],
                    'id': os.path.normpath(urlsplit(entry.links[0].href).path).split(os.sep).pop()} 
                    for entry in rss_data.entries]
        episodes, paginations = RSSClientUtil.extract_possible_paginations(entries)

        return RSSResponse(page_title, episodes, paginations)


    def get_episodes(self, show, page):
        response = requests.get(self._base_url + '/info/' + show + '/' + page)
        rss_data = feedparser.parse(response.content)

        page_title = rss_data.feed.title
        entries = [{'title': entry.title,
                    'id': os.path.normpath(urlsplit(entry.links[0].href).path).split(os.sep).pop()} 
                    for entry in rss_data.entries]
        episodes, paginations = RSSClientUtil.extract_possible_paginations(entries)

        return RSSResponse(page_title, episodes, paginations)


    def get_sources(self, episode):
        response = requests.get(self._base_url + '/episode/' + episode)
        rss_data = feedparser.parse(response.content)
            
        page_title = rss_data.feed.title
        entries = [{'title': entry.title,
                    'url': entry.links[0].href} 
                    for entry in rss_data.entries]

        return RSSResponse(page_title, entries)