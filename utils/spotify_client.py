from urllib.parse import urlencode
import requests
import base64
import datetime
import utils.External_functions as ef
import os


class SpotifyAPI(object):
    access_token = None
    access_token_expires = datetime.datetime.now()
    access_token_did_expire = True
    client_id = None
    client_secret = None
    token_url = "https://accounts.spotify.com/api/token"

    def __init__(self, client_id, client_secret, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret

    def get_client_credentials(self):
        """
        Returns a base64 encoded string
        """
        client_id = self.client_id
        client_secret = self.client_secret
        if client_secret == None or client_secret == None:
            raise Exception("You must set client_ID and client_secret")
        client_creds = f"{client_id}:{client_secret}"
        client_creds_base64 = base64.b64encode(client_creds.encode())
        return client_creds_base64.decode()

    def get_token_headers(self):
        client_creds_base64 = self.get_client_credentials()
        return {"Authorization": f"Basic {client_creds_base64}"}

    def get_token_data(self):
        return {"grant_type": "client_credentials"}

    def perfom_auth(self):
        token_url = self.token_url
        token_data = self.get_token_data()
        token_headers = self.get_token_headers()
        r = requests.post(token_url, data=token_data, headers=token_headers)
        if r.status_code not in range(200, 299):
            raise Exception("Could not authenticate client.")
        now = datetime.datetime.now()
        data = r.json()
        access_token = data["access_token"]
        expires_in = data["expires_in"]
        expires = now + datetime.timedelta(seconds=expires_in)
        self.access_token_expires = expires
        self.access_token_did_expire = expires < now
        self.access_token = access_token
        return True

    def get_access_token(self):
        token = self.access_token
        expires = self.access_token_expires
        now = datetime.datetime.now()
        if expires < now:
            self.perfom_auth()
            return self.get_access_token()
        elif token == None:
            self.perfom_auth()
            return self.get_access_token()
        return token

    async def spotify_track(self, link):
        access_token = self.get_access_token()
        id = link[31:53]
        headers = {"Authorization": f"Bearer {access_token}"}
        endpoint = "https://api.spotify.com/v1/tracks"

        lookup_url = f"{endpoint}/{id}"
        data = await ef.get_async(url=lookup_url, headers=headers, kind="json")
        if data is not None:
            track_name = data["name"]
            artist_name = data["artists"][0]["name"]
            return f"{track_name} - {artist_name}"

    async def spotify_track_lyric(self, link):
        access_token = self.get_access_token()
        id = link[31:53]
        headers = {"Authorization": f"Bearer {access_token}"}
        endpoint = "https://api.spotify.com/v1/tracks"

        lookup_url = f"{endpoint}/{id}"
        data = await ef.get_async(url=lookup_url, headers=headers, kind="json")
        if data is not None:
            track_name = data["name"]
            artist_name = data["artists"][0]["name"]
            return [track_name, artist_name]

    async def search(self, query, search_type="track"):
        access_token = self.get_access_token()
        headers = {"Authorization": f"Bearer {access_token}"}
        endpoint = "https://api.spotify.com/v1/search"
        data = urlencode(
            {"q": query, "type": search_type.lower(), "offset": 0, "limit": 1}
        )
        lookup_url = f"{endpoint}?{data}"
        data = await ef.get_async(url=lookup_url, headers=headers, kind="json")
        return data

    async def playlist(self, link, num, offset):
        link_main = link[34:]
        target_URI = ""
        for char in link_main:
            if char != "?":
                target_URI += char
            else:
                break
        access_token = self.get_access_token()
        headers = {"Authorization": f"Bearer {access_token}"}
        endpoint = "https://api.spotify.com/v1/playlists/"
        append = f"/tracks?market=ES&fields=items(track(name,artists,album(name,images)))&limit={num}&offset={offset}"
        lookup_url = f"{endpoint}{target_URI}{append}"
        data = await ef.get_async(lookup_url, headers=headers, kind="json")
        if data is None:
            return {}
        return data


client_id = os.getenv("spotify")
client_secret = os.getenv("spotify1")
spotify = SpotifyAPI(client_id, client_secret)


async def fetch_spotify_playlist(link, num):
    if num > 100:
        songs = []
        images = []
        album_names = []
        artist_names = []
        track_names = []
        loops_req = int(num // 100 + 1)
        offset = 0
        for loop in range(loops_req):
            data = await spotify.playlist(link=link, num=100, offset=offset)
            for item in range(100):
                try:
                    none_object = data["items"][item]["track"]
                except IndexError:
                    pass
                if none_object == None:
                    pass
                else:
                    try:
                        track_name = data["items"][item]["track"]["name"]
                        artist_name = data["items"][item]["track"]["artists"][0]["name"]
                        image = data["items"][item]["track"]["album"]["images"][1][
                            "url"
                        ]
                        album_name = data["items"][item]["track"]["album"]["name"]
                        songs.append(f"{track_name} - {artist_name}")
                        images.append(image)
                        album_names.append(album_name)
                        artist_names.append(artist_name)
                        track_names.append(track_name)
                        success = True
                    except IndexError:
                        pass
                    except Exception:
                        print(data)
            offset += 100
    else:
        songs = []
        images = []
        album_names = []
        artist_names = []
        track_names = []
        data = await spotify.playlist(link=link, num=num, offset=0)
        for item in range(num):
            try:
                track_name = data["items"][item]["track"]["name"]
                artist_name = data["items"][item]["track"]["artists"][0]["name"]
                image = data["items"][item]["track"]["album"]["images"][1]["url"]
                album_name = data["items"][item]["track"]["album"]["name"]
                songs.append(f"{track_name} - {artist_name}")
                images.append(image)
                album_names.append(album_name)
                artist_names.append(artist_name)
                track_names.append(track_name)
                success = True
            except IndexError:
                pass
            except Exception:
                print(data)
    # urls = []
    # base = 'https://www.youtube.com'
    # for song in songs:
    #     result = YoutubeSearch(song, max_results=1).to_dict()
    #     suffix = result[0]['url_suffix']
    #     link = base + suffix
    #     urls.append(link)
    return songs
