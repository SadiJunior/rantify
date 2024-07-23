import secrets

from flask import session

from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler


class SpotifyOAuthClient(SpotifyOAuth):
    """Spotify OAuth Client that handles the Spotify Authorization with Authorization Code Flow method."""

    def __init__(self):
        """Initializes the Spotify OAuth Client."""
        pass

    def init_app(self, app):
        """Initializes the Spotify OAuth Client with the given app."""
        super().__init__(
            client_id=app.config["SPOTIFY_CLIENT_ID"],
            client_secret=app.config["SPOTIFY_CLIENT_SECRET"],
            scope=app.config["SPOTIFY_SCOPE"],
            redirect_uri=app.config["SPOTIFY_REDIRECT_URI"],
            cache_handler=FlaskSessionCacheHandler(session),
            state=SpotifyOAuthClient.create_state(),
        )

    @staticmethod
    def create_state():
        """Creates a State used for Spotify OAuth."""
        return secrets.token_urlsafe(16)
