from dotenv import load_dotenv

from flask import Flask
from flask_session import Session

from config import configs_by_name

from app import errors, cache
from app.api.llm import LLMClient
from app.api.spotify_oauth import SpotifyOAuthClient


load_dotenv()


session = Session()
llm_client = LLMClient()
spotify_oauth = SpotifyOAuthClient()


def create_app(config_name="default"):
    """Create the Flask application."""
    app = Flask(__name__)
    app.config.from_object(configs_by_name[config_name])

    session.init_app(app)
    llm_client.init_app(app)
    spotify_oauth.init_app(app)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    from app.rant import bp as rant_bp
    app.register_blueprint(rant_bp, url_prefix="/rant")

    errors.init_app(app)
    cache.init_app(app)

    return app
