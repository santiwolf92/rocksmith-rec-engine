import os
import requests
import pandas as pd
import subprocess
from pathlib import Path
from dotenv import load_dotenv

# === Load credentials from .env ===
load_dotenv(dotenv_path=Path(__file__).parent / ".env")
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

# === Paths and flags ===
repo_root = Path(__file__).resolve().parent.parent
output_file = repo_root / "data" / "spotify_liked.csv"
AUTO_COMMIT = True

def get_access_token():
    refresh_token = os.getenv("SPOTIFY_REFRESH_TOKEN")
    auth_url = "https://accounts.spotify.com/api/token"
    response = requests.post(
        auth_url,
        data={
            "grant_type": "refresh_token",
            "refresh_token": refresh_token
        },
        auth=(CLIENT_ID, CLIENT_SECRET)
    )
    response.raise_for_status()
    return response.json()["access_token"]


# === Step 2: Fetch liked songs ===
def fetch_liked_songs(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    endpoint = "https://api.spotify.com/v1/me/tracks"
    params = {"limit": 50, "offset": 0}
    all_tracks = []

    while True:
        response = requests.get(endpoint, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        for item in data["items"]:
            track = item["track"]
            all_tracks.append({
                "Track URI": track["uri"],
                "Track Name": track["name"],
                "Album Name": track["album"]["name"],
                "Artist Name(s)": ", ".join(artist["name"] for artist in track["artists"]),
                "Release Date": track["album"]["release_date"],
                "Duration (ms)": track["duration_ms"],
                "Popularity": track["popularity"],
                "Explicit": track["explicit"],
                "Added By": item.get("added_by", {}).get("id", ""),
                "Added At": item["added_at"],
                "Genres": "",  # Spotify's public liked tracks API doesn't return genres
                "Record Label": "",  # Not available from this endpoint
                "Danceability": "",
                "Energy": "",
                "Key": "",
                "Loudness": "",
                "Mode": "",
                "Speechiness": "",
                "Acousticness": "",
                "Instrumentalness": "",
                "Liveness": "",
                "Valence": "",
                "Tempo": "",
                "Time Signature": ""
            })

        if data["next"] is None:
            break
        params["offset"] += params["limit"]

    return pd.DataFrame(all_tracks)

# === Main ===
if __name__ == "__main__":
    token = get_access_token()
    df = fetch_liked_songs(token)
    df.to_csv(output_file, index=False)
    print(f"[OK] Saved {len(df)} liked songs to: {output_file}")

    if AUTO_COMMIT:
        try:
            subprocess.run(["git", "-C", str(repo_root), "add", "data/spotify_liked.csv"], check=True)
            diff_result = subprocess.run(["git", "-C", str(repo_root), "diff", "--cached", "--quiet"], check=False)
            if diff_result.returncode != 0:
                subprocess.run(["git", "-C", str(repo_root), "commit", "-m", "🔄 Update Spotify liked songs"], check=True)
                subprocess.run(["git", "-C", str(repo_root), "push"], check=True)
                print("[OK] Git commit & push successful.")
            else:
                print("[SKIP] No changes to commit.")
        except subprocess.CalledProcessError as e:
            print(f"[!] Git operation failed: {e}")
