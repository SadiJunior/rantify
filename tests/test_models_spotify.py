from pydantic import HttpUrl

from app.models.spotify import SpotifyUser, SpotifyTrack, SpotifyArtist, SpotifyAlbum, SpotifyPlaylist


def test_create_spotify_user():
    """Test that a Spotify User can be created."""
    spotify_user_sample = {
        "country": "string",
        "display_name": "John Doe",
        "email": "string",
        "explicit_content": {"filter_enabled": False, "filter_locked": False},
        "external_urls": {"spotify": "string"},
        "followers": {"href": "string", "total": 0},
        "href": "string",
        "id": "1234567890",
        "images": [
            {"url": "https://i.scdn.co/image/ab67616d00001e02ff9ca10b55ce82ae553c8228", "height": 300, "width": 300}
        ],
        "product": "string",
        "type": "string",
        "uri": "string",
    }

    spotify_user = SpotifyUser.from_json(spotify_user_sample)

    assert spotify_user.id == "1234567890"
    assert spotify_user.name == "John Doe"
    assert spotify_user.image_url == HttpUrl("https://i.scdn.co/image/ab67616d00001e02ff9ca10b55ce82ae553c8228")


def test_create_spotify_track():
    """Test that a Spotify Track can be created."""
    spotify_track_sample = {
        "album": {
            "album_type": "compilation",
            "total_tracks": 9,
            "available_markets": ["CA", "BR", "IT"],
            "external_urls": {"spotify": "string"},
            "href": "string",
            "id": "2up3OPMp9Tb4dAKM2erWXQ",
            "images": [
                {"url": "https://i.scdn.co/image/ab67616d00001e02ff9ca10b55ce82ae553c8228", "height": 300, "width": 300}
            ],
            "name": "string",
            "release_date": "1981-12",
            "release_date_precision": "year",
            "restrictions": {"reason": "market"},
            "type": "album",
            "uri": "spotify:album:2up3OPMp9Tb4dAKM2erWXQ",
            "artists": [
                {
                    "external_urls": {"spotify": "string"},
                    "href": "string",
                    "id": "string",
                    "name": "string",
                    "type": "artist",
                    "uri": "string",
                }
            ],
        },
        "artists": [
            {
                "external_urls": {"spotify": "string"},
                "href": "string",
                "id": "string",
                "name": "string",
                "type": "artist",
                "uri": "string",
            }
        ],
        "available_markets": ["string"],
        "disc_number": 0,
        "duration_ms": 1000,
        "explicit": False,
        "external_ids": {"isrc": "string", "ean": "string", "upc": "string"},
        "external_urls": {"spotify": "string"},
        "href": "string",
        "id": "1234567890",
        "is_playable": True,
        "linked_from": {},
        "restrictions": {"reason": "string"},
        "name": "Lorem Ipsum",
        "popularity": 10,
        "preview_url": "string",
        "track_number": 0,
        "type": "track",
        "uri": "string",
        "is_local": False,
    }

    spotify_track = SpotifyTrack.from_json(spotify_track_sample)

    assert spotify_track.id == "1234567890"
    assert spotify_track.name == "Lorem Ipsum"
    assert spotify_track.popularity == 10
    assert spotify_track.explicit is False
    assert spotify_track.artists == [
        SpotifyArtist.from_json(artist_data) for artist_data in spotify_track_sample.get("artists", [])
    ]
    assert spotify_track.album == SpotifyAlbum.from_json(spotify_track_sample.get("album"))
    assert spotify_track.duration_ms == 1000
    assert spotify_track.is_playable is True
    assert spotify_track.is_local is False


def test_create_spotify_artist():
    """Test that a Spotify Artist can be created."""
    spotify_artist_sample = {
        "external_urls": {"spotify": "string"},
        "followers": {"href": "string", "total": 0},
        "genres": ["Prog rock", "Grunge"],
        "href": "string",
        "id": "1234567890",
        "images": [
            {"url": "https://i.scdn.co/image/ab67616d00001e02ff9ca10b55ce82ae553c8228", "height": 300, "width": 300}
        ],
        "name": "John Doe",
        "popularity": 0,
        "type": "artist",
        "uri": "string",
    }

    spotify_artist = SpotifyArtist.from_json(spotify_artist_sample)

    assert spotify_artist.id == "1234567890"
    assert spotify_artist.name == "John Doe"
    assert spotify_artist.genres == ["Prog rock", "Grunge"]
    assert spotify_artist.image_url == HttpUrl("https://i.scdn.co/image/ab67616d00001e02ff9ca10b55ce82ae553c8228")


def test_create_spotify_album():
    """Test that a Spotify Album can be created."""
    spotify_album_sample = {
        "album_type": "compilation",
        "total_tracks": 9,
        "available_markets": ["CA", "BR", "IT"],
        "external_urls": {"spotify": "string"},
        "href": "string",
        "id": "2up3OPMp9Tb4dAKM2erWXQ",
        "images": [
            {"url": "https://i.scdn.co/image/ab67616d00001e02ff9ca10b55ce82ae553c8228", "height": 300, "width": 300}
        ],
        "name": "Lorem Ipsum",
        "release_date": "1981-12",
        "release_date_precision": "year",
        "restrictions": {"reason": "market"},
        "type": "album",
        "uri": "spotify:album:2up3OPMp9Tb4dAKM2erWXQ",
        "artists": [
            {
                "external_urls": {"spotify": "string"},
                "href": "string",
                "id": "string",
                "name": "string",
                "type": "artist",
                "uri": "string",
            }
        ],
        "tracks": {
            "href": "https://api.spotify.com/v1/me/shows?offset=0&limit=20",
            "limit": 20,
            "next": "https://api.spotify.com/v1/me/shows?offset=1&limit=1",
            "offset": 0,
            "previous": "https://api.spotify.com/v1/me/shows?offset=1&limit=1",
            "total": 4,
            "items": [
                {
                    "artists": [
                        {
                            "external_urls": {"spotify": "string"},
                            "href": "string",
                            "id": "string",
                            "name": "string",
                            "type": "artist",
                            "uri": "string",
                        }
                    ],
                    "available_markets": ["string"],
                    "disc_number": 0,
                    "duration_ms": 0,
                    "explicit": False,
                    "external_urls": {"spotify": "string"},
                    "href": "string",
                    "id": "string",
                    "is_playable": False,
                    "linked_from": {
                        "external_urls": {"spotify": "string"},
                        "href": "string",
                        "id": "string",
                        "type": "string",
                        "uri": "string",
                    },
                    "restrictions": {"reason": "string"},
                    "name": "string",
                    "preview_url": "string",
                    "track_number": 0,
                    "type": "string",
                    "uri": "string",
                    "is_local": False,
                }
            ],
        },
        "copyrights": [{"text": "string", "type": "string"}],
        "external_ids": {"isrc": "string", "ean": "string", "upc": "string"},
        "genres": ["Egg punk", "Noise rock"],
        "label": "Cool Label",
        "popularity": 10,
    }

    spotify_album = SpotifyAlbum.from_json(spotify_album_sample)

    assert spotify_album.id == "2up3OPMp9Tb4dAKM2erWXQ"
    assert spotify_album.name == "Lorem Ipsum"
    assert spotify_album.album_type == "compilation"
    assert spotify_album.release_date == "1981-12"
    assert spotify_album.release_date_precision == "year"
    assert spotify_album.total_tracks == 9
    assert spotify_album.genres == ["Egg punk", "Noise rock"]
    assert spotify_album.label == "Cool Label"
    assert spotify_album.popularity == 10
    assert spotify_album.artists == [
        SpotifyArtist.from_json(artist_data) for artist_data in spotify_album_sample.get("artists", [])
    ]


def test_create_spotify_playlist():
    """Test that a Spotify Playlist can be created."""
    spotify_playlist_sample = {
        "collaborative": False,
        "description": "Lorem Ipsum Dolor Sit Amet",
        "external_urls": {"spotify": "string"},
        "followers": {"href": "string", "total": 0},
        "href": "string",
        "id": "1234567890",
        "images": [
            {"url": "https://i.scdn.co/image/ab67616d00001e02ff9ca10b55ce82ae553c8228", "height": 300, "width": 300}
        ],
        "name": "Lorem Ipsum",
        "owner": {
            "external_urls": {"spotify": "string"},
            "followers": {"href": "string", "total": 0},
            "href": "string",
            "id": "0987654321",
            "type": "user",
            "uri": "string",
            "display_name": "string",
        },
        "public": True,
        "snapshot_id": "string",
        "tracks": {
            "href": "https://api.spotify.com/v1/me/shows?offset=0&limit=20",
            "limit": 20,
            "next": "https://api.spotify.com/v1/me/shows?offset=1&limit=1",
            "offset": 0,
            "previous": "https://api.spotify.com/v1/me/shows?offset=1&limit=1",
            "total": 4,
            "items": [
                {
                    "added_at": "string",
                    "added_by": {
                        "external_urls": {"spotify": "string"},
                        "followers": {"href": "string", "total": 0},
                        "href": "string",
                        "id": "string",
                        "type": "user",
                        "uri": "string",
                    },
                    "is_local": False,
                    "track": {
                        "album": {
                            "album_type": "compilation",
                            "total_tracks": 9,
                            "available_markets": ["CA", "BR", "IT"],
                            "external_urls": {"spotify": "string"},
                            "href": "string",
                            "id": "2up3OPMp9Tb4dAKM2erWXQ",
                            "images": [
                                {
                                    "url": "https://i.scdn.co/image/ab67616d00001e02ff9ca10b55ce82ae553c8228",
                                    "height": 300,
                                    "width": 300,
                                }
                            ],
                            "name": "string",
                            "release_date": "1981-12",
                            "release_date_precision": "year",
                            "restrictions": {"reason": "market"},
                            "type": "album",
                            "uri": "spotify:album:2up3OPMp9Tb4dAKM2erWXQ",
                            "artists": [
                                {
                                    "external_urls": {"spotify": "string"},
                                    "href": "string",
                                    "id": "string",
                                    "name": "string",
                                    "type": "artist",
                                    "uri": "string",
                                }
                            ],
                        },
                        "artists": [
                            {
                                "external_urls": {"spotify": "string"},
                                "href": "string",
                                "id": "string",
                                "name": "string",
                                "type": "artist",
                                "uri": "string",
                            }
                        ],
                        "available_markets": ["string"],
                        "disc_number": 0,
                        "duration_ms": 0,
                        "explicit": False,
                        "external_ids": {"isrc": "string", "ean": "string", "upc": "string"},
                        "external_urls": {"spotify": "string"},
                        "href": "string",
                        "id": "string",
                        "is_playable": False,
                        "linked_from": {},
                        "restrictions": {"reason": "string"},
                        "name": "string",
                        "popularity": 0,
                        "preview_url": "string",
                        "track_number": 0,
                        "type": "track",
                        "uri": "string",
                        "is_local": False,
                    },
                }
            ],
        },
        "type": "string",
        "uri": "string",
    }

    spotify_playlist_tracks_sample = spotify_playlist_sample.get("tracks").get("items")

    spotify_playlist = SpotifyPlaylist.from_json(spotify_playlist_sample, spotify_playlist_tracks_sample)

    assert spotify_playlist.id == "1234567890"
    assert spotify_playlist.name == "Lorem Ipsum"
    assert spotify_playlist.owner_id == "0987654321"
    assert spotify_playlist.description == "Lorem Ipsum Dolor Sit Amet"
    assert spotify_playlist.image_url == HttpUrl("https://i.scdn.co/image/ab67616d00001e02ff9ca10b55ce82ae553c8228")
    assert spotify_playlist.public is True
    assert spotify_playlist.collaborative is False
    assert (
        spotify_playlist.tracks == [
            SpotifyTrack.from_json(track_data.get("track"))
            for track_data in spotify_playlist_tracks_sample
            if track_data.get("track")
        ]
        if spotify_playlist_tracks_sample
        else []
    )
