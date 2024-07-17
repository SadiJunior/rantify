from flask import (
    redirect, render_template, request
)

from spotipy.oauth2 import SpotifyOAuth, SpotifyOauthError

from langchain.schema.output_parser import OutputParserException

from helpers.app import session_helper
from helpers.app.error_helper import apology
from helpers.spotify import spotify_helper
from helpers.llm import rant_helper
from helpers.llm.llm_helper import LLMClient

from models.llm_models import RantType


def handle_rant(llm_client: LLMClient, playlist_id: str, rant_type: RantType):
    """Handles and generates the review of the given playlist."""
    try:
        rant = rant_helper.generate_rant(llm_client, playlist_id, rant_type)
    except (ValueError, OutputParserException):
        return apology("An error occurred while generating the rant", 500)

    match rant_type:
        case RantType.RATE | RantType.ROAST:
            return render_template("review.html", review=rant)
        case RantType.RHYME:
            return render_template("rhyme.html", rhyme=rant)
        case _:
            return apology("Invalid rant type", 400)


def handle_spotify_callback(spotify_oauth: SpotifyOAuth):
    """Callback from Spotify Authorization Code Flow."""
    state, code = SpotifyOAuth.parse_auth_response_url(request.url)

    try:
        token_info = spotify_helper.get_access_token(spotify_oauth, code)
    except (ValueError, SpotifyOauthError):
        return apology(f"Could not authorize your Spotify Account, please try again.", 400)

    session_helper.set_token_info(token_info)

    return redirect("/")
