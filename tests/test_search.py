from elasticsearch import exceptions as es_exceptions
from website.search import client as search_client


def test_query_index(client, monkeypatch):
    def mockreturn(*args, **kwargs):
        return [
            {"_id": 21344, "image": "fakeImageUrl1", "title": "ShowTitle1"},
            {"_id": 21345, "image": "fakeImageUrl2", "title": "ShowTitle2"},
        ]

    monkeypatch.setattr("website.search.routes.query_index", mockreturn)

    response = client.get("/search?q=test")
    assert response.status_code == 200
    assert len(response.json) == 2


def test_no_elasticsearch_config(monkeypatch):
    monkeypatch.setattr("website.search.client.current_app.elasticsearch", None)

    response = search_client.query_index("test")
    assert not response


def test_query_index_with_results(monkeypatch):
    def mockreturn(*args, **kwargs):
        source = {
            "id": 23231,
            "image": "imageUrl",
            "title": "Running Man (VI) (Cantonese)",
        }
        return {"hits": {"hits": [{"_source": source}]}}

    monkeypatch.setattr(
        "website.search.client.current_app.elasticsearch.search", mockreturn
    )

    response = search_client.query_index("test")
    assert response
    assert len(response) == 1


def test_search_service_down(client, monkeypatch):
    def mockreturn(*args, **kwargs):
        raise es_exceptions.ConnectionError

    monkeypatch.setattr(
        "website.search.client.current_app.elasticsearch.search", mockreturn
    )

    response = client.get("/search?q=test")
    assert response.status_code == 500
    assert "Search service is temporarily down" == response.data.decode()
