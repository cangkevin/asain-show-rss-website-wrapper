import logging

from flask import current_app

logger = logging.getLogger(__name__)


def query_index(query):
    if not current_app.elasticsearch:
        return []
    search = current_app.elasticsearch.search(
        index='listings',
        filter_path=['hits.hits._source'],
        body={'query': {'match': {'title': query}}},
        track_total_hits=False,
        size=5,
        track_scores=True,
        sort='_score:desc'
    )
    logger.info(search)
    results = [result['_source'] for result in search['hits']['hits']]
    return results
