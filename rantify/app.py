import os

from requests.exceptions import ReadTimeout

from flask import (
    Flask, redirect, render_template, request, session, jsonify
)
from flask_session import Session

from spotipy import SpotifyException, SpotifyOauthError

from dotenv import load_dotenv

from helpers.app import session_helper
from helpers.app.app_helper import handle_rant, handle_spotify_callback
from helpers.spotify import spotify_helper
from helpers.spotify.spotify_helper import SpotifyClient
from helpers.llm.llm_helper import LLMClient

from helpers.app.error_helper import apology

from models.spotify_models import SpotifyUser, SpotifyPlaylist
from models.llm_models import RantType


LLM_MODEL = "gpt-3.5-turbo"


# Loads the .env file
load_dotenv()


# Create application
app = Flask(__name__)


# Configure application cookies
app.secret_key = os.getenv("SECRET_KEY")
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SECURE"] = True

# Debug configs
app.jinja_env.auto_reload = True
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure server-side session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_USE_SIGNER"] = True
app.config["SESSION_TYPE"] = "filesystem"  # Use Redis or another backend for production


# Initializes session
Session(app)


spotify_oauth = spotify_helper.create_spotify_oauth()

llm_client = LLMClient(model=LLM_MODEL)


@app.route("/")
@session_helper.auth_required()
@session_helper.validate_token(spotify_oauth)
def index():
    """Index page of the application."""
    access_token = session_helper.get_access_token()
    spotify = SpotifyClient(access_token)

    user = spotify.get_user_profile()
    playlists = spotify.get_playlists(
        user.id,
        only_user_playlists=False,
        include_tracks=False,
    )

    return render_template("index.html", user=user, playlists=playlists)


@app.route("/login")
@session_helper.redirect_if_auth("/")
def login():
    """Login page of the application."""
    return render_template("login.html")


@app.route("/authorize", methods=["POST"])
@session_helper.redirect_if_auth("/")
def authorize():
    """Runs Autorization Code Flow for Logging user in Spotify Account."""
    authorize_url = spotify_oauth.get_authorize_url()

    return redirect(authorize_url)


@app.route("/callback")
@session_helper.redirect_if_auth("/")
def callback():
    """Callback from Spotify Authorization Code Flow."""
    return handle_spotify_callback(spotify_oauth)


@app.route("/logout")
@session_helper.auth_required()
def logout():
    """Log user out"""
    session_helper.clear_session()

    return redirect("/")


@app.route("/rate", methods=["POST"])
@session_helper.auth_required(from_ajax=True)
@session_helper.validate_token(spotify_oauth, from_ajax=True)
def rate():
    """Generates a rate about a playlist."""
    playlist_id = request.form.get("playlist")

    return handle_rant(llm_client, playlist_id, RantType.RATE)


@app.route("/roast", methods=["POST"])
@session_helper.auth_required(from_ajax=True)
@session_helper.validate_token(spotify_oauth, from_ajax=True)
def roast():
    """Generates a roast about a playlist."""
    playlist_id = request.form.get("playlist")

    return handle_rant(llm_client, playlist_id, RantType.ROAST)


@app.route("/rhyme", methods=["POST"])
@session_helper.auth_required(from_ajax=True)
@session_helper.validate_token(spotify_oauth, from_ajax=True)
def rhyme():
    """Generates a rhyme about a playlist."""
    playlist_id = request.form.get("playlist")

    return handle_rant(llm_client, playlist_id, RantType.RHYME)


@app.errorhandler(ReadTimeout)
def read_timeout(error):
    return apology(f"Authentication error", 400)
    

@app.errorhandler(SpotifyException)
def spotify_error(error):
    return apology(f"Spotify error {error.msg}", error.http_status)


@app.errorhandler(SpotifyOauthError)
def spotify_oauth_error(error):
    session_helper.clear_session()
    return apology(f"Authentication error: {error.error_description}", 400)


@app.errorhandler(404)
def page_not_found(error):
    return apology("Page not found", error.code)


@app.errorhandler(405)
def method_not_allowed(error):
    return apology("Method not allowed", error.code)
