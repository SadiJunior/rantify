from flask.testing import FlaskClient
from pytest_mock import MockerFixture


def test_login_redirect_if_not_auth(client: FlaskClient):
    """Test that the index page requires login."""
    with client.session_transaction() as session:
        session.clear()
        assert session.get("token_info") is None

    response = client.get("/")

    assert response.status_code == 302
    assert response.location == "auth/login"


def test_index_page(client: FlaskClient, spotify_token, mocker: MockerFixture):
    """Test the index page of the application."""
    with client.session_transaction() as session:
        session["token_info"] = spotify_token
        assert session.get("token_info") == spotify_token

    mock_spotify = mocker.patch("spotipy.Spotify", autospec=True)
    spotify_instance = mock_spotify.return_value
    spotify_instance.current_user.return_value = {
        "id": "1234567890",
        "display_name": "John Doe",
        "images": [{"url": "https://i.scdn.co/image/ab67616d00001e02ff9ca10b55ce82ae553c8228"}],
    }
    spotify_instance.user_playlists.return_value = {
        "items": [
            {
                "id": "0001",
                "name": "My Playlist 1",
                "owner": {"id": "1234567890"},
            },
            {
                "id": "0002",
                "name": "My Playlist 2",
                "owner": {"id": "1234567890"},
            },
            {
                "id": "0003",
                "name": "My Playlist 3",
                "owner": {"id": "1234567890"},
            },
        ],
        "next": None,
    }

    response = client.get("/")

    assert response.status_code == 200
    assert b'src="https://i.scdn.co/image/ab67616d00001e02ff9ca10b55ce82ae553c8228"' in response.data
    assert b'value="0001"' in response.data
    assert b'value="0002"' in response.data
    assert b'value="0003"' in response.data
    assert b"My Playlist 1" in response.data
    assert b"My Playlist 2" in response.data
    assert b"My Playlist 3" in response.data
