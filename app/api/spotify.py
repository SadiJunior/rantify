import spotipy

from app.models.spotify import SpotifyUser, SpotifyPlaylist


class SpotifyClient:
    """Spotify Client that gets parsed Spotify Data from the Spotify API."""

    def __init__(self, access_token):
        """Creates the Spotify Client object."""
        self.spotify_api_client = SpotifyAPIClient(access_token)

    def get_user_profile(self):
        """Gets the Spotify Current User data."""
        user_data = self.spotify_api_client.get_user_profile()

        return SpotifyUser.from_json(user_data)

    def get_playlists(self, user_id=None, only_user_playlists=True, include_tracks=True):
        """Gets the Spotify Current User's Playlists data."""
        playlists_data = self.spotify_api_client.get_playlists(user_id, only_user_playlists)

        if not include_tracks:
            return [SpotifyPlaylist.from_json(playlist_data) for playlist_data in playlists_data]

        return [
            SpotifyPlaylist.from_json(playlist_data, self.spotify_api_client.get_playlist_tracks(playlist_data["id"]))
            for playlist_data in playlists_data
        ]

    def get_playlist(self, playlist_id, include_tracks=True):
        """Gets the Spotify Playlist data."""
        playlist_data = self.spotify_api_client.get_playlist(playlist_id)

        if not include_tracks:
            return SpotifyPlaylist.from_json(playlist_data)

        tracks_data = self.spotify_api_client.get_playlist_tracks(playlist_id)
        return SpotifyPlaylist.from_json(playlist_data, tracks_data)


class SpotifyAPIClient:
    """Spotify Client that interacts directly with the Spotify API and returns it's raw JSON contents."""

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
