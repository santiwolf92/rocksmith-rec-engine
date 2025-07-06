"""
analyze.py

Main analysis script for the Rocksmith Recommendation Engine.
It compares your CDLC library with Spotify and Last.fm listening data,
and outputs high-priority song and artist recommendations.
"""

import pandas as pd
from pathlib import Path

# === 0. Encoding fixer ===
def fix_mojibake(text):
    if isinstance(text, str):
        try:
            return text.encode('utf-8').decode('utf-8')  # Forces utf-8 consistency
        except UnicodeDecodeError:
            return text
    return text

# === 1. Load Your Data ===

BASE_PATH = Path(__file__).resolve().parent.parent / 'data'

cdlc_df = pd.read_csv(BASE_PATH / 'cdlc_library.csv')
liked_df = pd.read_csv(BASE_PATH / 'spotify_liked.csv')
top_df = pd.read_csv(BASE_PATH / 'spotify_top.csv')

# Load lastfm data and fix encoding
lastfm_df = pd.read_csv(BASE_PATH / 'lastfm_top_artists.csv', encoding='latin1')
lastfm_df = lastfm_df.applymap(fix_mojibake)
# === 2. Normalize Artist and Track Names ===

def normalize(text):
    if not isinstance(text, str):
        return ''
    return text.strip().lower().replace('&', 'and')

cdlc_df['Artist Name(s)'] = cdlc_df['Artist Name(s)'].apply(normalize)
cdlc_df['Track Name'] = cdlc_df['Track Name'].apply(normalize)

liked_df['Artist Name(s)'] = liked_df['Artist Name(s)'].apply(normalize)
liked_df['Track Name'] = liked_df['Track Name'].apply(normalize)

top_df['Artist Name(s)'] = top_df['Artist Name(s)'].apply(normalize)
top_df['Track Name'] = top_df['Track Name'].apply(normalize)

lastfm_df['Artist Name(s)'] = lastfm_df['Artist Name(s)'].apply(normalize)

# === 3. Build Listening Profile ===

# Combine all Spotify tracks into one list of "known favorites"
all_spotify = pd.concat([liked_df[['Artist Name(s)', 'Track Name']],
                         top_df[['Artist Name(s)', 'Track Name']]]).drop_duplicates()

# Merge Last.fm artist data
artist_priority = lastfm_df[['Artist Name(s)', 'Scrobbles']]
artist_priority['Scrobbles'] = pd.to_numeric(artist_priority['Scrobbles'], errors='coerce')
artist_priority = artist_priority.dropna().sort_values(by='Scrobbles', ascending=False)

# === 4. Cross-Match ===

# Which favorite Spotify songs are missing in your CDLCs?
merged = pd.merge(all_spotify,
                  cdlc_df,
                  left_on=['Artist Name(s)', 'Track Name'],
                  right_on=['Artist Name(s)', 'Track Name'],
                  how='left',
                  indicator=True)

missing_songs = merged[merged['_merge'] == 'left_only'][['Artist Name(s)', 'Track Name']].drop_duplicates()

# Tag artist priority (from Last.fm)
missing_songs = missing_songs.merge(artist_priority,
                                    left_on='Artist Name(s)',
                                    right_on='Artist Name(s)',
                                    how='left')

# === 5. Output Recommendation Preview ===

top_recommendations = missing_songs.sort_values(by='Scrobbles', ascending=False).head(50)

print("ð¯ Top Missing Songs from Your Favorite Artists:\n")
for _, row in top_recommendations.iterrows():
    artist = row['Artist Name(s)'].title()
    song = row['Track Name'].title()
    scrobbles = int(row['Scrobbles']) if pd.notna(row['Scrobbles']) else '?'
    print(f"- {artist} â {song}  ({scrobbles} scrobbles)")

# Save CSV
output_dir = BASE_PATH / 'recommendations'
output_dir.mkdir(exist_ok=True)
top_recommendations.to_csv(output_dir / 'recommendations.csv', index=False)

print("\nâ Saved to data/recommendations/recommendations.csv")
