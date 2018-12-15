from website import create_app


def test_landing_page_should_redirect(client):
    response = client.get('/')
    assert response.status_code == 302
