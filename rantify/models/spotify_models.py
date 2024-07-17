from pydantic import BaseModel, HttpUrl
from typing import List, Optional


class SpotifyUser(BaseModel):
    """
    Modelates the Spotify Current User data.
    
    https://developer.spotify.com/documentation/web-api/reference/get-current-users-profile
    """
    id: Optional[str]
    name: Optional[str]
    image_url: Optional[HttpUrl]

    @classmethod
    def from_json(cls, user_data):
        """Creates a SpotifyUser object from the Spotify Current User data."""
        id = user_data.get("id")
        name = user_data.get("display_name")
        
        user_images = user_data.get("images")
        image_url = user_images[0]["url"] if user_images else "../static/images/default-user.png"

        return cls(
            id=id,
            name=name,
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

    @classmethod
    def from_json(cls, artist_data):
        """Creates a SpotifyArtist object from the Spotify Artist data."""
        id = artist_data.get("id")
        name = artist_data.get("name")
        genres = artist_data.get("genres")

        artist_images = artist_data.get("images")
        image_url = artist_images[0]["url"] if artist_images else None

        return cls(
            id=id,
            name=name,
            genres=genres,
            image_url=image_url,
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
