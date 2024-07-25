from flask import Flask

from requests.exceptions import ReadTimeout
from spotipy import SpotifyException, SpotifyOauthError

from app.helpers.session import clear_session
from app.helpers.errors import apology


def init_app(app: Flask):
    """Initialize global error handlers."""

    @app.errorhandler(ReadTimeout)
    def read_timeout(error):
        """Handle read timeout errors."""
        return apology("Authentication error", 400)


    @app.errorhandler(SpotifyException)
    def spotify_error(error):
        """Handle Spotify API errors."""
        return apology(f"Spotify error: {error.msg}", error.http_status)


    @app.errorhandler(SpotifyOauthError)
    def spotify_oauth_error(error):
        """Handle Spotify OAuth errors."""
        clear_session()
        return apology(f"Authentication error: {error.error_description}", 400)


    @app.errorhandler(404)
    def page_not_found(error):
        """Handle 404 errors."""
        return apology("Page not found", error.code)


    @app.errorhandler(405)
    def method_not_allowed(error):
        """Handle 405 errors."""
        return apology("Method not allowed", error.code)
