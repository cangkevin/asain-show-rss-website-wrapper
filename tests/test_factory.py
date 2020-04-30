def test_config(app, client):
    assert app.config["TESTING"]
    assert app.config["BASE_URL"] == "http://base_url/"
    assert client is not None
