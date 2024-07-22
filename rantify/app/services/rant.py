from flask import render_template

from langchain.schema.output_parser import OutputParserException

from app import llm_client
from app.helpers.session import get_access_token
from app.helpers.errors import apology
from app.api.spotify import SpotifyClient
from app.models.llm import Review, Rhyme, RantType


def handle_rant(playlist_id: str, rant_type: RantType):
    """Handles and generates the review of the given playlist."""
    try:
        rant = generate_rant(playlist_id, rant_type)
    except (ValueError, OutputParserException):
        return apology("An error occurred while generating the rant", 500)

    match rant_type:
        case RantType.RATE | RantType.ROAST:
            return render_template("rant/review.html", review=rant)
        case RantType.RHYME:
            return render_template("rant/rhyme.html", rhyme=rant)
        case _:
            return apology("Invalid rant type", 400)


def generate_rant(playlist_id: str, rant_type: RantType) -> Review | Rhyme:
    """Generates a Rant for the given playlist."""
    if not playlist_id:
        raise ValueError("Playlist not specified")
    
    access_token = get_access_token()
    spotify = SpotifyClient(access_token)

    playlist = spotify.get_playlist(playlist_id, include_tracks=True)

    if not playlist:
        raise ValueError("Playlist not found")
    
    try:
        match rant_type:
            case RantType.RATE:
                return llm_client.rate(playlist)

            case RantType.ROAST:
                return llm_client.roast(playlist)

            case RantType.RHYME:
                return llm_client.rhyme(playlist)
    except OutputParserException:
        raise
    
    return None
        