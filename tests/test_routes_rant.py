from flask.testing import FlaskClient
from pytest_mock import MockerFixture


def test_rant_routes_redirect_if_not_auth(client: FlaskClient, spotify_token):
    """Test that the rant routes are redirected to login if not authorized."""
    with client.session_transaction() as session:
        session["token_info"] = spotify_token
        assert session.get("token_info") is not None

    with client.session_transaction() as session:
        session.clear()
        assert session.get("token_info") is None

    response = client.post("/rant/rate")
    assert response.status_code == 401
    assert response.location == "/auth/login"

    response = client.post("/rant/roast")
    assert response.status_code == 401
    assert response.location == "/auth/login"

    response = client.post("/rant/rhyme")
    assert response.status_code == 401
    assert response.location == "/auth/login"
