import os

from requests.exceptions import ReadTimeout

from flask import (
    Flask, redirect, render_template, request, session, jsonify
)
from flask_session import Session

from spotipy import SpotifyException, SpotifyOauthError

from dotenv import load_dotenv

from helpers import session_helper, spotify_helper, rant_helper
from helpers.spotify_helper import SpotifyClient, SpotifyPlaylist, SpotifyUser
from helpers.llm_helper import LLMClient
from helpers.rant_helper import RantType
from helpers.error_helper import apology



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

    user_data = spotify.get_user_profile()
    user = SpotifyUser.from_json(user_data)

    playlists_data = spotify.get_playlists(user.id)
    playlists = [SpotifyPlaylist.from_json(playlist_data) for playlist_data in playlists_data]

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
    error = request.args.get("error")
    if error:
        return apology("Could not authorize your Spotify Account, please try again.", 400)

    code = request.args.get("code")
    if not code:
        return apology("Could not authorize your Spotify Account, please try again.", 400)

    try:
        token_info = spotify_oauth.get_access_token(code=code)
        if not token_info:
            return apology("Could not get token info", 400)
    except SpotifyOauthError as error:
        return apology(f"Error getting access token: {error.error_description}", 400)

    session_helper.set_token_info(token_info)

    return redirect("/")


@app.route("/logout")
@session_helper.auth_required()
def logout():
    """Log user out"""

    # Clears the session and forget the TOKEN INFO
    session_helper.clear_session()

    return redirect("/")


@app.route("/rate", methods=["POST"])
@session_helper.auth_required(from_ajax=True)
@session_helper.validate_token(spotify_oauth, from_ajax=True)
def rate():
    """Generates a rate about a playlist."""
    playlist_id = request.form.get("playlist")

    return rant_helper.handle_rant(llm_client, playlist_id, RantType.RATE)


@app.route("/roast", methods=["POST"])
@session_helper.auth_required(from_ajax=True)
@session_helper.validate_token(spotify_oauth, from_ajax=True)
def roast():
    """Generates a roast about a playlist."""
    playlist_id = request.form.get("playlist")

    return rant_helper.handle_rant(llm_client, playlist_id, RantType.ROAST)


@app.route("/rhyme", methods=["POST"])
@session_helper.auth_required(from_ajax=True)
@session_helper.validate_token(spotify_oauth, from_ajax=True)
def rhyme():
    """Generates a rhyme about a playlist."""
    playlist_id = request.form.get("playlist")

    return rant_helper.handle_rant(llm_client, playlist_id, RantType.RHYME)


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
