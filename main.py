from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth


CLIENT_ID = #YOUR CLIENT ID
CLIENT_SECRET = #YOUR CLIENT SECRET

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

#BILLBOARD
#STEP 1
#Scraping the Billboard Hot 100

response = requests.get("https://www.billboard.com/charts/hot-100/" + date)
top100_website = response.text
soup = BeautifulSoup(top100_website, "html.parser")
top100 = soup.select(selector="li ul li h3")
songs_list = [song.getText().strip() for song in top100]

#SPOTIFY
#STEP 2
#In order to create a playlist in Spotify you must have an account with Spotify.
#Then create a new Spotify App on this website: https://developer.spotify.com/dashboard/

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="playlist-modify-private",
                                               client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri="https://example.com",
                                               show_dialog=True,
                                               cache_path="token.txt"
                                               )
                     )

#STEP 3
#You will be taken to the example.com and then you need to copy the entire URL and paste it into the prompt in PyCharm (Terminal)
#Then you should see a new file in this project called token.txt

#STEP 4
#Get the user id of the authenticated user (your Spotify username)
user_id = sp.current_user()["id"]

#STEP 5
#Search Spotify for the Songs from STEP 1
song_names = songs_list
song_uris = []

year = date.split("-")[0]

for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

#STEP 6
#Create a new playlist

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
#print(playlist)

#Add each of the songs to the new playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)