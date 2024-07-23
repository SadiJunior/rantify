from flask import redirect, request

from spotipy.oauth2 import SpotifyOAuth, SpotifyOauthError

from app import spotify_oauth
from app.helpers.errors import apology
from app.helpers.session import set_token_info


def handle_spotify_callback():
    """Callback from Spotify Authorization Code Flow."""
    try:
        state, code = SpotifyOAuth.parse_auth_response_url(request.url)
        token_info = spotify_oauth.get_access_token(code)
    except (ValueError, SpotifyOauthError):
        return apology(f"Could not authorize your Spotify Account, please try again.", 400)

    set_token_info(token_info)

    return redirect("/")
