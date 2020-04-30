"""Models used throughout the application.

This module holds various model classes that are
intended for internal use.

"""
from collections import namedtuple

RssResponse = namedtuple("RssResponse", "title items paginations")
