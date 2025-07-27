import requests
import pandas as pd
from pathlib import Path

API_KEY = "6f8742e558ad32dae99f51f3fb923910"
USERNAME = "Santi_wolf"
PAGES = 1  # Increase if needed (each page = 1000 artists)

def fetch_lastfm_artists(api_key, username, pages=1):
    all_artists = []

    for page in range(1, pages + 1):
        url = "http://ws.audioscrobbler.com/2.0/"
        params = {
            "method": "library.getartists",
            "user": username,
            "api_key": api_key,
            "format": "json",
            "limit": 1000,
            "page": page,
        }

        response = requests.get(url, params=params)
        response.raise_for_status()

        data = response.json()
        artists = data.get("artists", {}).get("artist", [])
        for artist in artists:
            all_artists.append({
                "Artist Name(s)": artist["name"],
                "Scrobbles": int(artist["playcount"]),
            })

    return pd.DataFrame(all_artists)

if __name__ == "__main__":
    df = fetch_lastfm_artists(API_KEY, USERNAME, pages=PAGES)

    # ✅ Save to engine data path
    output_path = Path(__file__).resolve().parent.parent / "data" / "lastfm_top_artists.csv"
    df.to_csv(output_path, index=False)
    print(f"✅ Last.fm artist scrobble data saved to: {output_path}")
