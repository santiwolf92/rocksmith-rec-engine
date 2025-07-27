import requests
import pandas as pd
from pathlib import Path
import subprocess

# === CONFIGURATION ===
API_KEY = "6f8742e558ad32dae99f51f3fb923910"
USERNAME = "Santi_wolf"
PAGES = 1  # Increase if needed (each page = 1000 artists)
AUTO_COMMIT = True  # Set to False if you don’t want auto-commit/push

# === FUNCTIONS ===
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

# === MAIN ===
if __name__ == "__main__":
    df = fetch_lastfm_artists(API_KEY, USERNAME, pages=PAGES)

    # Save to correct data path in repo
    repo_root = Path(__file__).resolve().parent.parent
    file_path = repo_root / "data" / "lastfm_top_artists.csv"
    df.to_csv(file_path, index=False)
    print(f"[OK] Last.fm artist scrobble data saved to: {file_path}")

    if AUTO_COMMIT:
    try:
        subprocess.run(["git", "-C", str(repo_root), "add", "data/lastfm_top_artists.csv"], check=True)

        # Check if any changes actually exist
        diff_result = subprocess.run(
            ["git", "-C", str(repo_root), "diff", "--cached", "--quiet"],
            check=False
        )

        if diff_result.returncode != 0:
            subprocess.run(["git", "-C", str(repo_root), "commit", "-m", "🔄 Update Last.fm artist scrobble data"], check=True)
            subprocess.run(["git", "-C", str(repo_root), "push"], check=True)
            print("[OK] Git commit & push successful.")
        else:
            print("[SKIP] No changes to commit.")

    except subprocess.CalledProcessError as e:
        import sys
        print(f"[!] Git operation failed: {e}", file=sys.stderr)
