from flask import redirect, request

from spotipy.oauth2 import SpotifyOAuth, SpotifyOauthError, SpotifyStateError

from app import spotify_oauth
from app.helpers.errors import apology
from app.helpers.session import set_token_info


def handle_spotify_callback():
    """Callback from Spotify Authorization Code Flow."""
    try:
        state, code = SpotifyOAuth.parse_auth_response_url(request.url)

        if state is None or state != spotify_oauth.state:
            raise SpotifyStateError(message="Invalid state")

        token_info = spotify_oauth.get_access_token(code)
    except (ValueError, SpotifyOauthError, SpotifyStateError):
        return apology(f"Could not authorize your Spotify Account, please try again.", 400)

    set_token_info(token_info)

    return redirect("/")
