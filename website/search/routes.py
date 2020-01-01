import logging

from flask import request, jsonify
from website.search import bp
from website.search.client import query_index

logger = logging.getLogger(__name__)


@bp.route('/search')
def search_shows():
    query = request.args.get('q')
    logger.info('Search query: %s', query)
    response = query_index(query)
    return jsonify(response)
