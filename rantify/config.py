import os

class Config(object):
    """Set Base Flask configuration variables."""
    SECRET_KEY = os.getenv("SECRET_KEY")

    # Cookie configurations
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_NAME = "user_session"

    # Session configurations
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_TYPE = "filesystem"

    # LLM configurations
    LLM_MODEL = os.getenv("OPENAI_LLM_MODEL")
    LLM_MAX_PROMPT_TOKENS = 12288
    LLM_MAX_RETRY_ATTEMPTS = 3

    # Spotify configurations
    SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
    SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
    SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")
    SPOTIFY_SCOPE = [
        "playlist-read-private", # Read access to user's private playlists.
        "playlist-read-collaborative", # Include collaborative playlists when requesting a user's playlists.
        "user-library-read", # Read access to a user's library.
    ]


class DevelopmentConfig(Config):
    """Set Development Flask configuration variables."""
    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True


class ProductionConfig(Config):
    """Set Production Flask configuration variables."""
    SESSION_COOKIE_SECURE = True


configs_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}