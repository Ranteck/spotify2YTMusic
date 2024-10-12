import os
import time
import json
import logging
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from ytmusicapi import YTMusic
from tqdm import tqdm

# Configuración de logging
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
        # Verificar la estructura de los datos
        formatted_tracks = []
        for track in tracks:
            try:
                formatted_tracks.append({
                    'name': track['track']['name'],
                    'artist': track['track']['artists'][0]['name']
                })
            except KeyError as e:
                logging.error(f"KeyError: {e} in track data: {track}")
        return formatted_tracks

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
        self.ytmusic = YTMusic('headers_auth.json')  # Asegúrate de tener este archivo configurado

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


def load_synced_items():
    try:
        with open('synced_items.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {'tracks': [], 'albums': [], 'artists': []}


def save_synced_items(synced_items):
    with open('synced_items.json', 'w') as f:
        json.dump(synced_items, f)


def sync_spotify_to_youtube_music():
    synced_items = load_synced_items()
    spotify = SpotifyClient()
    ytmusic = YouTubeMusicClient()

    # Sync liked tracks
    logging.info("Syncing liked tracks...")
    liked_tracks = spotify.get_liked_tracks()
    for track in tqdm(liked_tracks, desc="Liked Tracks"):
        track_id = f"{track['name']} - {track['artist']}"
        if track_id not in synced_items['tracks']:
            try:
                ytmusic.like_track(track)
                synced_items['tracks'].append(track_id)
                time.sleep(1)  # Rate limiting
            except Exception as e:
                logging.error(f"Error syncing track {track['name']}: {str(e)}")

    # Sync saved albums
    logging.info("Syncing saved albums...")
    saved_albums = spotify.get_saved_albums()
    for album in tqdm(saved_albums, desc="Saved Albums"):
        album_id = f"{album['name']} - {album['artist']}"
        if album_id not in synced_items['albums']:
            try:
                ytmusic.add_album(album)
                synced_items['albums'].append(album_id)
                time.sleep(1)  # Rate limiting
            except Exception as e:
                logging.error(f"Error syncing album {album['name']}: {str(e)}")

    # Sync followed artists
    logging.info("Syncing followed artists...")
    followed_artists = spotify.get_followed_artists()
    for artist in tqdm(followed_artists, desc="Followed Artists"):
        if artist['name'] not in synced_items['artists']:
            try:
                ytmusic.subscribe_to_artist(artist)
                synced_items['artists'].append(artist['name'])
                time.sleep(1)  # Rate limiting
            except Exception as e:
                logging.error(f"Error syncing artist {artist['name']}: {str(e)}")

    save_synced_items(synced_items)
    logging.info("Synchronization completed!")


if __name__ == "__main__":
    sync_spotify_to_youtube_music()
