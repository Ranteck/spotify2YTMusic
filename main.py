import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from ytmusicapi import YTMusic
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SpotifyClient:
    def __init__(self):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=os.getenv('SPOTIFY_CLIENT_ID'),
            client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
            redirect_uri='http://localhost:8888/callback',
            scope='user-library-read user-follow-read'
        ))

    def get_liked_tracks(self):
        tracks = []
        results = self.sp.current_user_saved_tracks()
        while results:
            tracks.extend(results['items'])
            if results['next']:
                results = self.sp.next(results)
            else:
                break
        return [{'name': track['track']['name'], 'artist': track['track']['artists'][0]['name']} for track in tracks]

    def get_saved_albums(self):
        albums = []
        results = self.sp.current_user_saved_albums()
        while results:
            albums.extend(results['items'])
            if results['next']:
                results = self.sp.next(results)
            else:
                break
        return [{'name': album['album']['name'], 'artist': album['album']['artists'][0]['name']} for album in albums]

    def get_followed_artists(self):
        artists = []
        results = self.sp.current_user_followed_artists()
        while results:
            artists.extend(results['artists']['items'])
            if results['artists']['next']:
                results = self.sp.next(results['artists'])
            else:
                break
        return [{'name': artist['name']} for artist in artists]

class YouTubeMusicClient:
    def __init__(self):
        self.ytmusic = YTMusic('headers_auth.json')  # Make sure to set up authentication first

    def like_track(self, track):
        search_results = self.ytmusic.search(f"{track['name']} {track['artist']}", filter='songs')
        if search_results:
            video_id = search_results[0]['videoId']
            self.ytmusic.rate_song(video_id, 'LIKE')
            logging.info(f"Liked track: {track['name']} by {track['artist']}")
        else:
            logging.warning(f"Could not find track: {track['name']} by {track['artist']}")

    def add_album(self, album):
        search_results = self.ytmusic.search(f"{album['name']} {album['artist']}", filter='albums')
        if search_results:
            album_id = search_results[0]['browseId']
            self.ytmusic.rate_playlist(album_id, 'LIKE')
            logging.info(f"Added album: {album['name']} by {album['artist']}")
        else:
            logging.warning(f"Could not find album: {album['name']} by {album['artist']}")

    def subscribe_to_artist(self, artist):
        search_results = self.ytmusic.search(artist['name'], filter='artists')
        if search_results:
            channel_id = search_results[0]['browseId']
            self.ytmusic.subscribe_artists([channel_id])
            logging.info(f"Subscribed to artist: {artist['name']}")
        else:
            logging.warning(f"Could not find artist: {artist['name']}")

def sync_spotify_to_youtube_music():
    spotify = SpotifyClient()
    ytmusic = YouTubeMusicClient()

    # Sync liked tracks
    logging.info("Syncing liked tracks...")
    liked_tracks = spotify.get_liked_tracks()
    for track in liked_tracks:
        ytmusic.like_track(track)

    # Sync saved albums
    logging.info("Syncing saved albums...")
    saved_albums = spotify.get_saved_albums()
    for album in saved_albums:
        ytmusic.add_album(album)

    # Sync followed artists
    logging.info("Syncing followed artists...")
    followed_artists = spotify.get_followed_artists()
    for artist in followed_artists:
        ytmusic.subscribe_to_artist(artist)

    logging.info("Synchronization completed!")

if __name__ == "__main__":
    sync_spotify_to_youtube_music()
