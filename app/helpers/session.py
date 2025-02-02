from flask import session

from spotipy.cache_handler import FlaskSessionCacheHandler


def get_token_info():
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
    return token_info["access_token"]


def pop_oauth_state():
    """Gets the SPOTIFY OAUTH STATE from the Flask session"""
    return session.pop("oauth_state", None)


def set_oauth_state(oauth_state):
    """Sets the given SPOTIFY OAUTH STATE inside the Flask session"""
    session["oauth_state"] = oauth_state


def clear_session():
    """Clears the session"""
    session.clear()
