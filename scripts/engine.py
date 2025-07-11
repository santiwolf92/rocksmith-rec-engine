import pandas as pd
import re
import requests
import time
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent / 'data'
OUTPUT_PATH = BASE_PATH / 'recommendations'

def fix_mojibake(text):
    if isinstance(text, str):
        try:
            return text.encode('latin1').decode('utf-8')
        except UnicodeDecodeError:
            return text
    return text

def normalize(text):
    if not isinstance(text, str):
        return ''
    text = text.lower().replace('&', 'and')
    return re.sub(r'[^a-z0-9]', '', text)

def cdlc_exists_on_customsforge(artist, track):
    query = f"{artist} {track}"
    payload = {
        "draw": 1,
        "columns[0][data]": "Add",
        "columns[0][name]": "",
        "columns[0][searchable]": "true",
        "columns[0][orderable]": "false",
        "columns[0][search][value]": "",
        "columns[0][search][regex]": "false",
        "search[value]": query,
        "search[regex]": "false",
        "start": 0,
        "length": 10,
    }

try:
    for attempt in range(3):
        response = requests.post("https://ignition4.customsforge.com/tablesettings", data=payload, timeout=10)
        if response.status_code != 200:
            continue

        try:
            data = response.json()
        except ValueError:
            print(f"⚠️ Invalid JSON for: {artist} — {track}")
            continue

        print(f"✅ Received response for: {artist} — {track}")

        for result in data.get("data", []):
            result_artist = result.get("Artist", "").lower()
            result_title = result.get("Title", "").lower()
            if artist.lower() in result_artist and track.lower() in result_title:
                return True

        time.sleep(0.5)
    return False

except Exception as e:
    print(f"⚠️ CustomsForge error for '{artist} – {track}': {e}")
    return False


def load_and_prepare_data():
    cdlc_df = pd.read_csv(BASE_PATH / 'cdlc_library.csv')
    liked_df = pd.read_csv(BASE_PATH / 'spotify_liked.csv')
    top_df = pd.read_csv(BASE_PATH / 'spotify_top.csv')
    lastfm_df = pd.read_csv(BASE_PATH / 'lastfm_top_artists.csv')
    lastfm_df = lastfm_df.apply(lambda col: col.map(fix_mojibake))

    for df in [cdlc_df, liked_df, top_df]:
        df['Artist Normalized'] = df['Artist Name(s)'].apply(normalize)
        df['Track Normalized'] = df['Track Name'].apply(normalize)
    lastfm_df['Artist Normalized'] = lastfm_df['Artist Name(s)'].apply(normalize)

    return cdlc_df, liked_df, top_df, lastfm_df

def generate_recommendations(top_n=50, save=True, min_scrobbles=0, max_scrobbles=None, filter_existing=False, update_progress=None):
    cdlc_df, liked_df, top_df, lastfm_df = load_and_prepare_data()

    all_spotify = pd.concat([
        liked_df[['Artist Name(s)', 'Track Name', 'Artist Normalized', 'Track Normalized']],
        top_df[['Artist Name(s)', 'Track Name', 'Artist Normalized', 'Track Normalized']]
    ]).drop_duplicates(subset=['Artist Normalized', 'Track Normalized'])

    artist_priority = lastfm_df[['Artist Name(s)', 'Scrobbles', 'Artist Normalized']]
    artist_priority = artist_priority.copy()
    artist_priority['Scrobbles'] = pd.to_numeric(artist_priority['Scrobbles'], errors='coerce')
    artist_priority = artist_priority.dropna()

    if max_scrobbles is not None:
        artist_priority = artist_priority[
            (artist_priority['Scrobbles'] >= min_scrobbles) & (artist_priority['Scrobbles'] <= max_scrobbles)
        ]
    else:
        artist_priority = artist_priority[artist_priority['Scrobbles'] >= min_scrobbles]

    artist_priority = artist_priority.sort_values(by='Scrobbles', ascending=False)

    merged = pd.merge(
        all_spotify,
        cdlc_df[['Artist Normalized', 'Track Normalized']],
        on=['Artist Normalized', 'Track Normalized'],
        how='left',
        indicator=True
    )

    missing_songs = merged[merged['_merge'] == 'left_only'][[
        'Artist Name(s)', 'Track Name', 'Artist Normalized']].drop_duplicates()

    missing_songs = missing_songs.merge(
        artist_priority[['Artist Name(s)', 'Scrobbles', 'Artist Normalized']],
        on='Artist Normalized',
        how='left',
        suffixes=('', '_LastFM')
    )

    recommendations = missing_songs.sort_values(by='Scrobbles', ascending=False)

    if filter_existing:
        filtered = []
        total = len(recommendations.head(top_n))
        for i, (_, row) in enumerate(recommendations.head(top_n).iterrows(), 1):
            artist = row['Artist Name(s)']
            track = row['Track Name']
            if update_progress:
                update_progress(i, total, artist, track)
            if cdlc_exists_on_customsforge(artist, track):
                filtered.append(row)
            time.sleep(1)
        if update_progress:
            update_progress(total, total, "Done", "")
        recommendations = pd.DataFrame(filtered)

    if recommendations.empty:
        print("\u26a0\ufe0f No filtered results were generated.")
        return pd.DataFrame(columns=['Artist Name(s)', 'Track Name', 'Scrobbles'])

    top_recommendations = recommendations.head(top_n)

    print("\U0001F3AF Top Missing Songs from Your Favorite Artists:\n")
    for _, row in top_recommendations.iterrows():
        artist = row['Artist Name(s)'].title()
        song = row['Track Name'].title()
        scrobbles = int(row['Scrobbles']) if pd.notna(row['Scrobbles']) else '?'
        print(f"- {artist} — {song}  ({scrobbles} scrobbles)")

    if save:
        OUTPUT_PATH.mkdir(exist_ok=True)
        output_file = OUTPUT_PATH / 'recommendations.csv'
        top_recommendations[['Artist Name(s)', 'Track Name', 'Scrobbles']].to_csv(output_file, index=False)
        print(f"\n✅ Saved to {output_file}")

    print("\u2705 Returning top recommendations")
    return top_recommendations

