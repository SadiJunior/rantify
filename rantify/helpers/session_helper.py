import os

from flask import redirect, session
from functools import wraps
from spotipy.oauth2 import SpotifyOAuth, SpotifyOauthError
from spotipy.cache_handler import FlaskSessionCacheHandler


SPOTIFY_TOKEN_INFO = "token_info"
SPOTIFY_ACCESS_TOKEN = "access_token"
SPOTIFY_OAUTH_STATE = "oauth_state"


def redirect_if_auth(location : str):
    """Decorate routes to redirect if already authorized"""
    def decorator_function(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # If user is authorized
            if get_token_info():
                return redirect(location)
            return f(*args, **kwargs)
        return decorated_function
    return decorator_function


def auth_required():
    """Decorate routes to require authorization"""
    def decorator_function(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # If session does not have Token Info, isn't authorized
            if not get_token_info():
                return redirect("/login")
            return f(*args, **kwargs)
        return decorated_function
    return decorator_function


def validate_token(spotify_oauth : SpotifyOAuth):
    """Decorate routes to validate token"""
    def decorator_function(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            """Validates the SPOTIFY TOKEN INFO. Refresh token if necessary"""
            session_token_info = get_token_info()
            if session_token_info and not spotify_oauth.is_token_expired(session_token_info):
                return f(*args, **kwargs)
        
            try:
                validated_token_info = spotify_oauth.validate_token(session_token_info)
                if not validated_token_info:
                    return redirect("/login")
            except SpotifyOauthError as e:
                return redirect("/login")

            set_token_info(validated_token_info)
            return f(*args, **kwargs)
        return decorated_function
    return decorator_function


def pop_oauth_state():
    """Gets the SPOTIFY OAUTH STATE from the Flask session"""
    return session.pop(SPOTIFY_OAUTH_STATE, None)


def set_oauth_state(oauth_state):
    """Sets the given SPOTIFY OAUTH STATE inside the Flask session"""
    session[SPOTIFY_OAUTH_STATE] = oauth_state


def get_token_info() -> str:
    """Gets the SPOTIFY TOKEN INFO from the Flask session"""
    cache_handler = FlaskSessionCacheHandler(session)
    return cache_handler.get_cached_token()


def set_token_info(token_info):
    """Sets the given SPOTIFY TOKEN INFO inside the Flask session"""
    cache_handler = FlaskSessionCacheHandler(session)
    cache_handler.save_token_to_cache(token_info)


def get_access_token():
    """Gets the access token from the SPOTIFY TOKEN INFO"""
    token_info = get_token_info()
    return token_info[SPOTIFY_ACCESS_TOKEN]


def clear_session():
    """Clears the session"""
    session.clear()
    
