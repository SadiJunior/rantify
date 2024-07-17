import csv

from typing import List
from io import StringIO

from models.spotify_models import SpotifyPlaylist, SpotifyTrack


def playlist_to_csv(playlist: SpotifyPlaylist):
    """Gets the Playlist data as CSV"""
    fields = ["Playlist Name", "Description", "Number of Tracks"]
    playlist_data = [[playlist.name, playlist.description, len(playlist.tracks)]]

    return get_csv_table(fields, playlist_data)


def tracks_to_csv(tracks: List[SpotifyTrack]):
    """Gets the Tracks data as CSV."""
    fields = ["Track Name", "Artist Names", "Album Name", "Release Date"]
    tracks_data = [get_track_data(track) for track in tracks]

    return get_csv_table(fields, tracks_data)


def get_csv_table(fields, tracks_data):
    """Gets a table as CSV string."""
    with StringIO() as string_io:
        writer = csv.writer(string_io)
        writer.writerow(fields)
        writer.writerows(tracks_data)

        return string_io.getvalue()


def get_track_data(track: SpotifyTrack):
    """Gets the track data that will be used for prompting."""
    if track is None:
        return []
    
    track_name = track.name
    artist_names = [artist.name if artist else None for artist in track.artists] if track.artists else None
    album_name = track.album.name if track.album else None
    album_release_date = track.album.release_date if track.album else None

    return [
        track_name,
        artist_names,
        album_name,
        album_release_date,
    ]
