from langchain.schema.output_parser import OutputParserException

from helpers.app import session_helper
from helpers.spotify.spotify_helper import SpotifyClient
from helpers.llm.llm_helper import LLMClient

from models.llm_models import RantType, Review, Rhyme


def generate_rant(llm_client: LLMClient, playlist_id: str, rant_type: RantType) -> Review | Rhyme:
    """Generates a Rant for the given playlist."""
    if not playlist_id:
        raise ValueError("Playlist not specified")
    
    access_token = session_helper.get_access_token()
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
        