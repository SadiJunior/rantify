from flask.testing import FlaskClient
from pytest_mock import MockerFixture


def test_login_page(client: FlaskClient):
    """Test that the login page loads."""
    with client.session_transaction() as session:
        assert session.get("token_info") is None

    response = client.get("/auth/login")

    assert response.status_code == 200
    assert b"Rantify" in response.data
    assert b"Log in with Spotify" in response.data


def test_login_redirect_if_auth(client: FlaskClient, spotify_token):
    """Test that the login page redirects if authorized."""
    with client.session_transaction() as session:
        session["token_info"] = spotify_token

    response = client.get("/auth/login")

    assert response.status_code == 302
    assert response.location == "/"


def test_logout_clears_session(client: FlaskClient, spotify_token):
    """Test that the logout page clears the session."""
    with client.session_transaction() as session:
        session["token_info"] = spotify_token

    response = client.get("/auth/logout")

    assert response.status_code == 302
    assert response.location == "/"

    with client.session_transaction() as session:
        assert session.get("token_info") is None


def test_logout_redirect_if_not_auth(client: FlaskClient):
    """Test that the logout page redirects if not authorized."""
    with client.session_transaction() as session:
        assert session.get("token_info") is None

    response = client.get("/auth/logout")

    assert response.status_code == 302
    assert response.location == "/auth/login"


def test_spotify_authorize_redirect(client: FlaskClient):
    """Test that the spotify authorize redirects to the Spotify login page."""
    response = client.get("/auth/spotify/authorize")

    assert response.status_code == 302
    assert response.location.startswith("https://accounts.spotify.com/authorize")
    assert "state" in response.location


def test_spotify_callback(client: FlaskClient, spotify_token, mocker: MockerFixture):
    """Test that the Spotify callback saves the token info and redirects to home."""
    with client.session_transaction() as session:
        assert session.get("token_info") is None

        session["oauth_state"] = "dummy_state"

    mock_parse_auth_response_url = mocker.patch("spotipy.oauth2.SpotifyOAuth.parse_auth_response_url")
    mock_get_access_token = mocker.patch("spotipy.oauth2.SpotifyOAuth.get_access_token")

    mock_parse_auth_response_url.return_value = ("dummy_state", "dummy_code")
    mock_get_access_token.return_value = spotify_token

    response = client.get("/auth/spotify/callback", query_string={"code": "dummy_code", "state": "dummy_state"})

    assert response.status_code == 302
    assert response.location == "/"

    with client.session_transaction() as session:
        assert session.get("token_info") == spotify_token


def test_auth_pages_redirect_if_auth(client: FlaskClient, spotify_token):
    """Test that the auth pages are redirected to home if authorized."""
    with client.session_transaction() as session:
        session["token_info"] = spotify_token
        assert session.get("token_info") is not None

    response = client.get("/auth/login")
    assert response.status_code == 302
    assert response.location == "/"

    response = client.get("/auth/spotify/authorize")
    assert response.status_code == 302
    assert response.location == "/"

    response = client.get("/auth/spotify/callback")
    assert response.status_code == 302
    assert response.location == "/"
