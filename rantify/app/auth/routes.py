from flask import redirect, render_template

from app import spotify_oauth
from app.auth import bp
from app.decorators.session import auth_required, redirect_if_auth
from app.services.spotify import handle_spotify_callback
from app.helpers.session import clear_session


@bp.route("/login")
@redirect_if_auth("/")
def login():
    """Login page of the application."""
    return render_template("auth/login.html")


@bp.route("/spotify/authorize", methods=["POST"])
@redirect_if_auth("/")
def authorize():
    """Runs Autorization Code Flow for Logging user in Spotify Account."""
    authorize_url = spotify_oauth.get_authorize_url()

    return redirect(authorize_url)


@bp.route("/spotify/callback")
@redirect_if_auth("/")
def callback():
    """Callback from Spotify Authorization Code Flow."""
    return handle_spotify_callback()


@bp.route("/logout")
@auth_required()
def logout():
    """Log user out"""
    clear_session()

    return redirect("/")
