"""Models used throughout the application.

This module holds various model classes that are
intended for internal use.

"""


class RSSResponse:
    '''Model that encapsulates a resource'''
    def __init__(self, title, items, paginations=None):
        self.title = title
        self.items = items
        self.paginations = paginations
