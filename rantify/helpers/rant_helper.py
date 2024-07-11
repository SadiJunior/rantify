from enum import Enum

from spotipy.exceptions import SpotifyException
from langchain.schema.output_parser import OutputParserException

from flask import render_template

from helpers import session_helper
from helpers.error_helper import apology
from helpers.spotify_helper import SpotifyClient, SpotifyPlaylist


class RantType(Enum):
    """The type of Rant to generate."""
    RATE = 0
    ROAST = 1


# TODO: Find a better way for implementing this.
def handle_review(llm_client, playlist_id, rant_type):
    """Handles and generates the review of the given playlist."""
    if not playlist_id:
        return apology("Playlist not found", 400)
    
    access_token = session_helper.get_access_token()
    spotify = SpotifyClient(access_token)

    try:
        playlist = SpotifyPlaylist.from_json(
            spotify.get_playlist(playlist_id),
            spotify.get_playlist_tracks(playlist_id),
        )
    except SpotifyException as e:
        return apology("Playlist data not found: " + e.msg, 400)

    if not playlist:
        return apology("Playlist data not found", 400)
    
    review = None

    try:
        match rant_type:
            case RantType.RATE:
                review = llm_client.rate(playlist)

            case RantType.ROAST:
                review = llm_client.roast(playlist)
    except OutputParserException:
        return apology("Internal error when generating rate", 500)

    return render_template("review.html", review=review)