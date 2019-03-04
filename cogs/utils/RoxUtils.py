import aiohttp
import asyncio
from bs4 import BeautifulSoup as BS
from googleapiclient.discovery import build
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import re

class ThumbNailer(object):

    def __init__(self):
        self.url = self

    async def connection(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=30) as response:
                assert response.status == 200
                html = await response.read()
                return ThumbNailer.__parse_result(html)

    def __parse_result(html):
        try:
            soup = BS(html, 'html.parser')
            img = soup.find("meta", property="twitter:image")["content"]
            return img
        except Exception as e:
            raise e

    async def identify(self, identifier, uri):
        thumbnail_url = ""
        if "youtube" in uri:
            thumbnail_url = f"https://img.youtube.com/vi/{identifier}/0.jpg"
            return thumbnail_url
        elif "soundcloud" in uri:
            thumbnail_url = await ThumbNailer.connection(ThumbNailer, url=uri)
            return thumbnail_url
        else:
            return None



def thumbnailer(self, identifier, uri):
    thumbnail_url = ""
    if "youtube" in uri:
        thumbnail_url = f"https://img.youtube.com/vi/{identifier}/0.jpg"
        return thumbnail_url
    elif "soundcloud" in uri:
        thumbnail_url = BS(requests.get(uri).text, "html.parser").find("meta", property="twitter:image")["content"]
        return thumbnail_url
    else:
        return None

class _Youtube:
    async def _search(self, search, max_results):
        youtube = build('youtube', "v3", developerKey=self.youtube["dev_key"])
        search_response = youtube.search().list(
            q=search,
            part='id',
            maxResults=max_results,
            type='video'
            ).execute()

        print(f"search_response: {search_response}")
        for search_result in search_response.get('items', []):
            if search_result['id']['kind'] == 'youtube#video':
                print(f"search_result: {search_result['id']['videoId']}")
                return search_result['id']['videoId']
            if search_result["pageInfo"]["totalResults"] == 0:
                print(f"search_result None")
                break

    async def name2id(self, names):
        _ids = []
        print(f"name2id.names: {names}")
        if isinstance(names, list):
            print(f"name2id.names: list_true")
            for pos in range(len(names)):
                _ids.append(await _Youtube._search(self, names[pos], 1))
        elif isinstance(names, str):
            print(f"name2id.names: str_true")
            _ids.append(await _Youtube._search(self, names, 1))
        else:
            print(f"{type(names)} is not a accepted datatype")
            return None
        print(f"name2id._ids: {_ids}")
        return _ids


class _Spotify:
    def client(self):
        manager = SpotifyClientCredentials(self.spotify["client_id"], self.spotify["secret"])
        client = spotipy.Spotify(client_credentials_manager=manager)
        return client

    async def idfy(self, data):
        user_name = None; playlist_id = None
        print(f"idfy: {data}")
        if "playlist" in data:
            if "/" in data:
                uri = data.split("/")
                user_name = uri[4]
                try:
                    playlist_id = uri[6].split("?")[0]
                except:
                    playlist_id = uri[6]
            elif ":" in data:
                uri = data.split(':')
                user_name = uri[2]
                playlist_id = uri[4]
            return await _Spotify.playlist(self, user_name, playlist_id)

        elif "track" in data:
            return await _Spotify.song(self, data)

    async def song(self, song_):
        song = _Spotify.client(self).track(song_)
        print(f"song.song: {song}")
        print(f"song.song_: {song_}")
        name = song["name"]
        artist = song["artists"][0]["name"]
        album = song["album"]["name"]
        s_string = [f"{name} - {artist} - {album}"]
        _Spotify._info = {"song": name, "artist": artist}
        print(f"song.s_string: {s_string}")
        #print(_info)
        return s_string

    async def playlist(self, user, playlist):
        plist = _Spotify.client(self).user_playlist(user, playlist)
        songs = plist["tracks"]["items"]
        s_dict = []
        for i in range(min(len(songs), 10)):
            name = songs[i]["track"]["name"]
            artist = songs[i]["track"]["artists"][0]["name"]
            album = songs[i]["track"]["album"]["name"]
            s_dict.append(f"{name} - {artist} - {album}")
        return s_dict
