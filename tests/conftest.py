import pytest
import time

from flask import Flask

from app import create_app


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app("test")
    return app


@pytest.fixture
def client(app: Flask):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app: Flask):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()


@pytest.fixture
def spotify_token():
    """A dummy Spotify token payload."""
    payload = {
        "access_token": "dummy_access_token",
        "token_type": "Bearer",
        "expires_at": 3600,
        "refresh_token": "dummy_refresh_token",
        "scope": "playlist-read-collaborative playlist-read-private user-library-read",
        "expires_at": time.time() + 3600,
    }

    return payload
