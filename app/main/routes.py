from flask import render_template

from app.main import bp
from app.decorators.session import auth_required, validate_token
from app.api.spotify import SpotifyClient
from app.helpers.session import get_access_token


@bp.route("/")
@auth_required()
@validate_token()
def index():
    """Index page of the application."""
    access_token = get_access_token()
    spotify = SpotifyClient(access_token)

    user = spotify.get_user_profile()
    playlists = spotify.get_playlists(
        user.id,
        only_user_playlists=True,
        include_tracks=False,
    )

    return render_template("main/index.html", user=user, playlists=playlists)
