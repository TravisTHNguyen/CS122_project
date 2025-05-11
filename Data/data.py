import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import os
from pathlib import Path

CLIENT_ID = "d3b16b119e9547d6965785618bcf4543"
CLIENT_SECRET = "30e320c3376a4383ba5a25af9bc8cb2a"
REDIRECT_URI = "http://localhost:8080"
SCOPE = "playlist-read-private"

# Create data directory if it doesn't exist
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

playlist_map = {
    "2020": "7MyK3ZYElsc0Bkxlvbs8v0",
    "2021": "5hU11GCo5NWKLw8GcJrJI0",
    "2022": "7LK8Ahimzuz68GTnbcMeuU",
    "2023": "0Ddm828dFibjTld6eojSvR",
    "2024": "2LEWfVqIUsbBcwLzX1GzKs"
}

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE
))

for year, pid in playlist_map.items():
    all_data = []
    try:
        playlist = sp.playlist(pid)
        playlist_name = playlist['name']
        print(f"📥 Fetching: {playlist_name} ({year})")

        tracks = sp.playlist_items(pid, limit=100)["items"]

        for item in tracks:
            track = item['track']
            if not track:
                continue

            song = track["name"]
            artist_name = track["artists"][0]["name"]
            artist_id = track["artists"][0]["id"]
            popularity = track["popularity"]
            explicit = track["explicit"]
            duration_ms = track["duration_ms"]
            album_name = track["album"]["name"]
            release_date = track["album"]["release_date"]

            genres = []
            artist_popularity = None
            artist_followers = None

            if artist_id:
                try:
                    artist_info = sp.artist(artist_id)
                    genres = artist_info.get("genres", [])
                    artist_popularity = artist_info.get("popularity")
                    artist_followers = artist_info.get("followers", {}).get("total")
                except Exception as e:
                    print(f"⚠️ Error fetching artist data for {artist_name}: {e}")

            all_data.append({
                "Year": year,
                "Playlist": playlist_name,
                "Song": song,
                "Artist": artist_name,
                "Popularity": popularity,
                "Explicit": explicit,
                "Duration (ms)": duration_ms,
                "Album": album_name,
                "Release Date": release_date,
                "Artist Popularity": artist_popularity,
                "Artist Followers": artist_followers,
                "Genres": ", ".join(genres) if genres else "unknown"
            })

        output_path = DATA_DIR / f"{year}_playlist_data.csv"
        pd.DataFrame(all_data).to_csv(output_path, index=False)
        print(f"✅ Saved: {output_path}")

    except Exception as e:
        print(f"❌ Failed to process year {year}: {e}")