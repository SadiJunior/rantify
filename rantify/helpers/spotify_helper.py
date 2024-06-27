import os
import spotipy
import secrets

from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler

from flask import session


SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")


# https://developer.spotify.com/documentation/web-api/concepts/scopes
SPOTIFY_SCOPE = [
    "playlist-read-private", # Read access to user's private playlists.
    "playlist-read-collaborative", # Include collaborative playlists when requesting a user's playlists.
    "user-top-read", # Read access to a user's top artists and tracks.
    "user-read-recently-played", # Read access to a user’s recently played tracks.
    "user-library-read", # Read access to a user's library.
    "user-read-private", # Read access to user’s subscription details (type of user account).
]


def create_spotify_oauth() -> SpotifyOAuth:
    """
    Creates the Spotify Authorization with Authorization Code Flow method

    https://developer.spotify.com/documentation/web-api/concepts/authorization
    https://developer.spotify.com/documentation/web-api/tutorials/code-flow
    """
    return SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        scope=SPOTIFY_SCOPE,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        cache_handler=FlaskSessionCacheHandler(session),
    )


def create_state():
    return secrets.token_urlsafe(16)


def create_spotify_client(access_token):
    return spotipy.Spotify(
        auth=access_token
    )


def prompt_dict_keys(keys):
    def decorator(c):
        if not hasattr(c, "prompt_dict_keys"):
            c.prompt_dict_keys = []
        c.prompt_dict_keys.extend(keys)
        return c
    return decorator


class SpotifyClient:

    def __init__(self, access_token):
        self.spotify = create_spotify_client(access_token)


    def get_user_profile(self):
        return self.spotify.current_user()


    def get_playlists(self, user_id = None):
        if user_id is None:
            user_id = self.get_user_profile()["id"]

        results = self.spotify.user_playlists(user_id)
        user_playlists = results["items"]

        while results["next"]:
            results = self.spotify.next(results)
            user_playlists.extend(results["items"])

        # Only gets playlists created by user
        user_playlists = [playlist for playlist in user_playlists if playlist["owner"]["id"] == user_id]
        
        return user_playlists


    def get_playlist(self, playlist_id):
        return self.spotify.playlist(playlist_id)
    

    def get_playlist_tracks(self, playlist_id):
        results = self.spotify.playlist_tracks(playlist_id)
        if not results:
            return []

        playlist_tracks = results["items"]

        while results["next"]:
            results = self.spotify.next(results)
            playlist_tracks.extend(results["items"])
        
        return playlist_tracks


    def get_user_top_tracks(self):
        return self.spotify.current_user_top_tracks()


    def get_user_top_artists(self):
        return self.spotify.current_user_top_artists()
    


class Serializable:

    def __init__(self):
        self.prompt_keys = []


    def to_dict(self):
        def serialize(obj):
            if isinstance(obj, Serializable):
                return obj.to_dict()
            elif isinstance(obj, list):
                return [serialize(item) for item in obj]
            elif isinstance(obj, dict):
                return {key: serialize(value) for key, value in obj.items()}
            else:
                return obj
        
        return serialize(self.__dict__)


    def to_prompt_dict(self):
        def serialize(obj):
            if isinstance(obj, Serializable):
                return obj.to_prompt_dict()
            elif isinstance(obj, list):
                return [serialize(item) for item in obj]
            elif isinstance(obj, dict):
                return {key: serialize(value) for key, value in obj.items() if key in self.prompt_keys}
            else:
                return obj
        
        return serialize(self.__dict__)


class SpotifyUser(Serializable):

    def __init__(self, user_data):
        self.id = user_data.get("id")
        self.name = user_data.get("display_name")
        self.country = user_data.get("country")
        
        user_images = user_data.get("images")
        self.image_url = user_images[0]["url"] if user_images else "../static/images/default-user.png"

        super().__init__()
        self.prompt_keys = ["name", "country"]
        


class SpotifyPlaylist(Serializable):

    def __init__(self, playlist_data, playlist_tracks_data = None):
        self.id = playlist_data.get("id")
        self.name = playlist_data.get("name")
        self.owner_id = playlist_data.get("owner").get("id")
        self.description = playlist_data.get("description")
        
        playlist_images = playlist_data.get("images")
        self.image_url = playlist_images[0]["url"] if playlist_images else None

        self.tracks = [SpotifyTrack(track_data.get("track")) for track_data in playlist_tracks_data] if playlist_tracks_data else None
        
        super().__init__()
        self.prompt_keys = ["name", "description", "tracks"]


class SpotifyTrack(Serializable):

    def __init__(self, track_data):
        self.id = track_data.get("id")
        self.name = track_data.get("name")
        self.popularity = track_data.get("popularity")
        self.is_explicit = bool(track_data.get("explicit"))

        self.artists = [SpotifyArtist(artist_data) for artist_data in track_data.get("artists")]

        album = track_data.get("album")
        self.album = SpotifyAlbum(album)

        super().__init__()
        self.prompt_keys = ["name", "popularity", "artists", "album"]


class SpotifyArtist(Serializable):

    def __init__(self, artist_data):
        self.id = artist_data.get("id")
        self.name = artist_data.get("name")

        super().__init__()
        self.prompt_keys = ["name"]


class SpotifyAlbum(Serializable):

    def __init__(self, album_data):
        self.id = album_data.get("id")
        self.name = album_data.get("name")
        self.release_date = album_data.get("release_date")
        self.total_tracks = album_data.get("total_tracks")

        super().__init__()
        self.prompt_keys = ["name", "release_date", "total_tracks"]
