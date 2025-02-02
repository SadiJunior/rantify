from flask import redirect, url_for
from functools import wraps

from spotipy.oauth2 import SpotifyOauthError

from app import spotify_oauth
from app.helpers.session import get_token_info, set_token_info


def redirect_if_auth(location: str):
    """Decorate routes to redirect if already authorized"""

    def decorator_function(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # If user is authorized
            session_token_info = get_token_info()
            if session_token_info and not spotify_oauth.is_token_expired(session_token_info):
                return redirect(location)
            return f(*args, **kwargs)

        return decorated_function

    return decorator_function


def auth_required(from_ajax: bool = False):
    """Decorate routes to require authorization"""

    def decorator_function(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # If session does not have Token Info, isn't authorized
            if not get_token_info():
                login_url = url_for("auth.login")
                return redirect(login_url, code=401) if from_ajax else redirect(login_url)
            return f(*args, **kwargs)

        return decorated_function

    return decorator_function


def validate_token(from_ajax: bool = False):
    """Decorate routes to validate token"""

    def decorator_function(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            """Validates the SPOTIFY TOKEN INFO. Refresh token if necessary"""
            session_token_info = get_token_info()
            if session_token_info and not spotify_oauth.is_token_expired(session_token_info):
                return f(*args, **kwargs)

            login_url = url_for("auth.login")

            try:
                validated_token_info = spotify_oauth.validate_token(session_token_info)
                if not validated_token_info:
                    return redirect(login_url, code=401) if from_ajax else redirect(login_url)
            except SpotifyOauthError:
                return redirect(login_url, code=401) if from_ajax else redirect(login_url)

            set_token_info(validated_token_info)
            return f(*args, **kwargs)

        return decorated_function

    return decorator_function
