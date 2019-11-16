'''
This module contains global constants.
'''

# file paths for mock data/response
MOVIES_RESP_FILE = 'tests/data/movie_response.txt'
SHOWS_RESP_FILE = 'tests/data/show_response.txt'
SINGLE_SHOW_FILE = 'tests/data/single_show.txt'
EPISODES_RESP_FILE = 'tests/data/episode_response.txt'
SOURCES_RESP_FILE = 'tests/data/sources_response.txt'
EMPTY_RESP_FILE = 'tests/data/empty_response.txt'

# template paths
MOVIES_TEMPLATE = 'core/movies.html'
SHOWS_TEMPLATE = 'core/shows.html'
EPISODES_TEMPLATE = 'core/episodes.html'
SOURCES_TEMPLATE = 'core/sources.html'
USER_ERROR_TEMPLATE = '404.html'
SERVER_ERROR_TEMPLATE = '500.html'

# subcategories for shows
DRAMA_SHOWS = {
    'hk-drama': 'HK Dramas',
    'c-drama': 'Chinese Dramas (English sub)',
    'c-drama-can-dub': 'Chinese Dramas (Cantonese dub)',
    'k-drama': 'Korean Dramas (English sub)',
    'tw-drama': 'Taiwanese Dramas (English sub)',
    'tw-drama-can-dub': 'Taiwanese Dramas (Cantonese dub)'
}

VARIETY_SHOWS = {
    'hk-show': 'HK Variety & News'
}

RECENTLY_ADDED_SHOWS = {
    'recently-added-can-dub': 'Recently Added (Cantonese dub)',
}

# encompass all subcategories of shows
SHOW_CATAGORIES = {
    'Dramas': DRAMA_SHOWS,
    'Variety & News': VARIETY_SHOWS,
    'Recently Updated Shows': RECENTLY_ADDED_SHOWS
}

# subcategories for movies
MOVIES = {
    'c-movies-can-dub': 'Chinese Movies (Cantonese dub)',
    'hk-movies': 'HK Movies',
    'recently-added-can-dub': 'Recently Added Movies (Cantonese dub)'
}

# encompass all subcategories of movies
MOVIE_CATAGORIES = {
    'Movies': MOVIES
}
