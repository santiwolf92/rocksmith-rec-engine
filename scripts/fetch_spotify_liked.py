import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
from pathlib import Path
import subprocess

# === CONFIGURATION ===
CLIENT_ID = "87e1c9eb2bf84b838fe692827a11b93a"
CLIENT_SECRET = "159984f022da4c4f8830fce7b7cbb920"
REDIRECT_URI = "http://localhost:8888/callback"
SCOPE = "user-library-read"
AUTO_COMMIT = True

def fetch_liked_songs():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE
    ))

    liked_songs = []
    limit = 50
    offset = 0

    while True:
        results = sp.current_user_saved_tracks(limit=limit, offset=offset)
        if not results['items']:
            break

        for item in results['items']:
            track = item['track']
            liked_songs.append({
                "Artist Name(s)": track['artists'][0]['name'],
                "Track Name": track['name'],
                "Album": track['album']['name'],
                "Added At": item['added_at'],
                "Spotify ID": track['id'],
                "Popularity": track['popularity'],
                "URI": track['uri']
            })

        offset += limit

    return pd.DataFrame(liked_songs)

if __name__ == "__main__":
    df = fetch_liked_songs()

    # Save
    repo_root = Path(__file__).resolve().parent.parent
    file_path = repo_root / "data" / "spotify_liked.csv"
    df.to_csv(file_path, index=False)
    print(f"[OK] Spotify liked songs saved to: {file_path}")

    if AUTO_COMMIT:
        try:
            subprocess.run(["git", "-C", str(repo_root), "add", "data/spotify_liked.csv"], check=True)
            subprocess.run(["git", "-C", str(repo_root), "commit", "-m", "🎵 Update Spotify liked songs"], check=True)
            subprocess.run(["git", "-C", str(repo_root), "push"], check=True)
            print("[OK] Git commit & push successful.")
        except subprocess.CalledProcessError as e:
            print(f"[!] Git operation failed: {e}")
