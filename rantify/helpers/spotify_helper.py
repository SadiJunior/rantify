import os
import spotipy
import secrets

from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler

from pydantic import BaseModel, HttpUrl
from typing import List, Optional

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
    Creates the Spotify Authorization with Authorization Code Flow method.

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
    """Creates a State used for Spotify OAuth."""
    return secrets.token_urlsafe(16)


class SpotifyClient:
    """Spotify Client that interacts with the Spotify API."""

    def __init__(self, access_token):
        """Creates the Spotify Client object."""
        self.spotify = spotipy.Spotify(access_token)


    def get_user_profile(self):
        """Gets the Spotify Current User data."""
        return self.spotify.current_user()


    def get_playlists(self, user_id=None, only_user_playlists=True):
        """Gets the Spotify Current User's Playlists data."""
        if user_id is None:
            user_id = self.get_user_profile()["id"]

        results = self.spotify.user_playlists(user_id)
        user_playlists = results["items"]

        while results["next"]:
            results = self.spotify.next(results)
            user_playlists.extend(results["items"])

        user_playlists = [playlist for playlist in user_playlists]

        if only_user_playlists:
            user_playlists = [playlist for playlist in user_playlists if playlist["owner"]["id"] == user_id]
        
        return user_playlists


    def get_playlist(self, playlist_id):
        """Gets the Spotify Playlist data."""
        return self.spotify.playlist(playlist_id)
    

    def get_playlist_tracks(self, playlist_id):
        """Gets the Spotify Playlist Tracks data."""
        results = self.spotify.playlist_tracks(playlist_id)
        if not results:
            return []

        playlist_tracks = results["items"]

        while results["next"]:
            results = self.spotify.next(results)
            playlist_tracks.extend(results["items"])
        
        return playlist_tracks


    def get_user_top_tracks(self):
        """Gets the Spotify Current User's Top Tracks data."""
        return self.spotify.current_user_top_tracks()


    def get_user_top_artists(self):
        """Gets the Spotify Current User's Top Artists data."""
        return self.spotify.current_user_top_artists()


class SpotifyUser(BaseModel):
    """
    Modelates the Spotify Current User data.
    
    https://developer.spotify.com/documentation/web-api/reference/get-current-users-profile
    """
    id: Optional[str]
    name: Optional[str]
    country: Optional[str]
    image_url: Optional[HttpUrl]

    @classmethod
    def from_json(cls, user_data):
        """Creates a SpotifyUser object from the Spotify Current User data."""
        id = user_data.get("id")
        name = user_data.get("display_name")
        country = user_data.get("country")
        
        user_images = user_data.get("images")
        image_url = user_images[0]["url"] if user_images else "../static/images/default-user.png"

        return cls(
            id=id,
            name=name,
            country=country,
            image_url=image_url
        )


class SpotifyArtist(BaseModel):
    """
    Model of the Spotify Artist data.

    https://developer.spotify.com/documentation/web-api/reference/get-an-artist
    """
    id: Optional[str]
    name: Optional[str]
    genres: Optional[List[str]]
    image_url: Optional[HttpUrl]
    popularity: Optional[int]

    @classmethod
    def from_json(cls, artist_data):
        """Creates a SpotifyArtist object from the Spotify Artist data."""
        id = artist_data.get("id")
        name = artist_data.get("name")
        genres = artist_data.get("genres")
        popularity = artist_data.get("popularity")

        artist_images = artist_data.get("images")
        image_url = artist_images[0]["url"] if artist_images else None

        return cls(
            id=id,
            name=name,
            genres=genres,
            image_url=image_url,
            popularity=popularity
        )


class SpotifyAlbum(BaseModel):
    """
    Model of the Spotify Album data.

    https://developer.spotify.com/documentation/web-api/reference/get-an-album
    """
    id: Optional[str]
    name: Optional[str]
    album_type: Optional[str]
    release_date: Optional[str]
    release_date_precision: Optional[str]
    total_tracks: Optional[int]
    genres: Optional[List[str]]
    label: Optional[str]
    popularity: Optional[int]
    artists: Optional[List[SpotifyArtist]]

    @classmethod
    def from_json(cls, album_data):
        """Creates a SpotifyAlbum object from the Spotify Album data."""
        id = album_data.get("id")
        name = album_data.get("name")
        album_type = album_data.get("album_type")
        release_date = album_data.get("release_date")
        release_date_precision = album_data.get("release_date_precision")
        total_tracks = album_data.get("total_tracks")
        genres = album_data.get("genres")
        label = album_data.get("label")
        popularity = album_data.get("popularity")

        artists = [SpotifyArtist.from_json(artist_data) for artist_data in album_data.get("artists", [])]

        return cls(
            id=id,
            name=name,
            album_type=album_type,
            release_date=release_date,
            release_date_precision=release_date_precision,
            total_tracks=total_tracks,
            genres=genres,
            label=label,
            popularity=popularity,
            artists=artists
        )


class SpotifyTrack(BaseModel):
    """
    Model of the Spotify Track data.

    https://developer.spotify.com/documentation/web-api/reference/get-track
    """
    id: Optional[str]
    name: Optional[str]
    popularity: Optional[int]
    explicit: Optional[bool]
    artists: Optional[List[SpotifyArtist]]
    album: Optional[SpotifyAlbum]
    duration_ms: Optional[int]
    is_playable: Optional[bool]
    is_local: Optional[bool]

    @classmethod
    def from_json(cls, track_data):
        """Creates a SpotifyTrack object from the Spotify Track data."""
        id = track_data.get("id")
        name = track_data.get("name")
        popularity = track_data.get("popularity")
        explicit = track_data.get("explicit")
        duration_ms = track_data.get("duration_ms")
        is_playable = track_data.get("is_playable")
        is_local = track_data.get("is_local")

        artists = [SpotifyArtist.from_json(artist_data) for artist_data in track_data.get("artists", [])]

        album_data = track_data.get("album")
        album = SpotifyAlbum.from_json(album_data)

        return cls(
            id=id,
            name=name,
            popularity=popularity,
            explicit=explicit,
            artists=artists,
            album=album,
            duration_ms=duration_ms,
            is_playable=is_playable,
            is_local=is_local
        )


class SpotifyPlaylist(BaseModel):
    """
    Model of the Spotify Playlist data.

    https://developer.spotify.com/documentation/web-api/reference/get-playlist
    """
    id: Optional[str]
    name: Optional[str]
    owner_id: Optional[str]
    description: Optional[str]
    image_url: Optional[HttpUrl]
    public: Optional[bool]
    collaborative: Optional[bool]
    tracks: Optional[List[SpotifyTrack]]

    @classmethod
    def from_json(cls, playlist_data, playlist_tracks_data=None):
        """Creates a SpotifyPlaylist object from the Spotify Playlist data."""
        id = playlist_data.get("id")
        name = playlist_data.get("name")
        owner_id = playlist_data.get("owner").get("id")
        description = playlist_data.get("description")
        public = playlist_data.get("public")
        collaborative = playlist_data.get("collaborative")
        
        playlist_images = playlist_data.get("images")
        image_url = playlist_images[0]["url"] if playlist_images else None

        tracks = [SpotifyTrack.from_json(track_data.get("track")) for track_data in playlist_tracks_data if track_data.get("track")] if playlist_tracks_data else []
        
        return cls(
            id=id,
            name=name,
            owner_id=owner_id,
            description=description,
            image_url=image_url,
            public=public,
            collaborative=collaborative,
            tracks=tracks
        )
