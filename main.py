from bs4 import BeautifulSoup
import requests
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint

date = input("Which year do you want to travel to? Type in the data in this format YYYY-MM-DD: ")

response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}")

top_songs = response.text

soup = BeautifulSoup(markup=top_songs, features="html.parser")

song_soup = soup.find_all(name="span", class_="chart-element__information__song text--truncate color--primary")

songs = [song.getText() for song in song_soup]

scope = "playlist-modify-private"
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=os.environ["SPOTIPY_CLIENT_ID"], 
        client_secret=os.environ["SPOTIPY_CLIENT_SECRET"], 
        redirect_uri=os.environ["SPOTIPY_REDIRECT_URI"],
        scope=scope,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]

year = date.split("-")[0]
song_uri_list = []
for song in songs:
    song_uri = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = song_uri["tracks"]["items"][0]["uri"]
        song_uri_list.append(uri)
    except IndexError:
        print("Song could not be found")

plist = sp.user_playlist_create(
    user=user_id,
    name=f"{date} Billboard 100",
    public=False,
    description=f"Top 100 songs from {date}. Some songs may be missing if they are not found on Spotify."
)

sp.playlist_add_items(
    playlist_id=plist["id"],
    items=song_uri_list
)