from flask.testing import FlaskClient
from requests.exceptions import ReadTimeout
from spotipy import SpotifyException, SpotifyOauthError


def test_read_timeout_error(client: FlaskClient):
    """Test the ReadTimeout error handler."""
    @client.application.route('/trigger-read-timeout')
    def trigger_read_timeout():
        raise ReadTimeout()

    response = client.get('/trigger-read-timeout')
    assert response.status_code == 400
    assert b"Authentication error" in response.data


def test_spotify_error(client: FlaskClient, spotify_token):
    """Test the SpotifyException error handler."""
    @client.application.route('/trigger-spotify-error')
    def trigger_spotify_error():
        raise SpotifyException(400, -1, "Spotify Error Triggered")

    with client.session_transaction() as session:
        session["token_info"] = spotify_token
        assert session.get("token_info") == spotify_token

    response = client.get('/trigger-spotify-error')

    assert response.status_code == 400
    assert b"Spotify error:" in response.data
    assert b"Spotify Error Triggered" in response.data

    with client.session_transaction() as session:
        assert session.get("token_info") is None


def test_spotify_oauth_error(client: FlaskClient, spotify_token, mocker):
    """Test the SpotifyOauthError error handler."""
    @client.application.route('/trigger-spotify-oauth-error')
    def trigger_spotify_oauth_error():
        error_msg = "Authentication Error Triggered"
        raise SpotifyOauthError(message=error_msg, error_description=error_msg)

    with client.session_transaction() as session:
        session["token_info"] = spotify_token
        assert session.get("token_info") == spotify_token

    response = client.get('/trigger-spotify-oauth-error')

    assert response.status_code == 400
    assert b"Authentication error:" in response.data
    assert b"Authentication Error Triggered" in response.data

    with client.session_transaction() as session:
        assert session.get("token_info") is None


def test_404_error(client):
    """Test the 404 error handler."""
    response = client.get('/non-existent-route')

    assert response.status_code == 404
    assert b"Page not found" in response.data


def test_405_error(client):
    """Test the 405 error handler."""
    @client.application.route('/trigger-method-not-allowed', methods=['GET'])
    def trigger_method_not_allowed():
        return "Hello"

    response = client.post('/trigger-method-not-allowed')
    assert response.status_code == 405
    assert b"Method not allowed" in response.data
