from flask_caching.backends.filesystemcache import FileSystemCache


def test_app_exists(app):
    """Test that the app exists."""
    assert app is not None


def test_app_is_testing(app):
    """Test that the app is in testing mode."""
    assert app.config["TESTING"]


def test_app_has_session_cookie_name(app):
    """Test that the app has a session cookie name."""
    assert app.config["SESSION_COOKIE_NAME"] == "user_session"


def test_app_has_session_cache(app):
    """Test that the app has a session cache."""
    assert app.config["SESSION_TYPE"] == "cachelib"

    cachelib = app.config["SESSION_CACHELIB"]

    assert isinstance(cachelib, FileSystemCache)
    assert cachelib._path == "/tmp/flask_session"


def test_app_has_secret_key(app):
    """Test that the app has a secret key."""
    assert app.config["SECRET_KEY"] is not None


def test_app_has_spotify_data(app):
    """Test that the app has Spotify data."""
    assert app.config["SPOTIFY_CLIENT_ID"] is not None
    assert app.config["SPOTIFY_CLIENT_SECRET"] is not None
    assert app.config["SPOTIFY_REDIRECT_URI"] is not None
    assert app.config["SPOTIFY_SCOPE"] is not None


def test_app_has_openai_data(app):
    """Test that the app has OpenAI data."""
    assert app.config["LLM_MODEL"] is not None
    assert app.config["LLM_MAX_PROMPT_TOKENS"] is not None
    assert app.config["LLM_MAX_RETRY_ATTEMPTS"] is not None
