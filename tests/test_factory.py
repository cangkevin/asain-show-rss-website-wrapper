def test_config(app, client):
    assert app.testing
    assert client is not None
