import os
import re
import shutil
import pandas as pd
from fuzzywuzzy import process, fuzz

# === PATHS ===
CDLC_FOLDER = r"C:\Program Files (x86)\Steam\steamapps\common\Rocksmith2014\dlc"
UNMATCHED_FOLDER = os.path.join(CDLC_FOLDER, "unmatched")
LOG_PATH = os.path.join("data", "rename_log.txt")

# === LOAD LISTENING HISTORY ===
def load_reference_titles():
    sources = ["data/lastfm_history.csv", "data/spotify_liked.csv"]
    titles = set()
    for path in sources:
        if os.path.exists(path):
            df = pd.read_csv(path)
            if 'Artist Name(s)' in df.columns and 'Track Name' in df.columns:
                df = df.rename(columns={'Artist Name(s)': 'artist', 'Track Name': 'track'})
                for artist, track in zip(df['artist'], df['track']):
                    titles.add(f"{artist.strip()} - {track.strip()}")
    return titles

# === NORMALIZATION ===
def normalize_filename(filename):
    name = re.sub(r'\[.*?\]|\(.*?\)|RS2014|v\d+|PART_REAL_GUITAR|_vocals|_lead|_rhythm|\.psarc', '', filename, flags=re.IGNORECASE)
    name = re.sub(r'[_\.]+', ' ', name)
    return name.strip().title()

def best_match(name, reference_titles):
    result = process.extractOne(name, reference_titles, scorer=fuzz.token_sort_ratio)
    if result is None:
        return None
    match, score = result
    return match if score >= 80 else None

# === MAIN LOGIC ===
def normalize_cdlc():
    os.makedirs(UNMATCHED_FOLDER, exist_ok=True)
    reference_titles = load_reference_titles()
    log_entries = []

    for root, _, files in os.walk(CDLC_FOLDER):
        for filename in files:
            if filename.lower().endswith(".psarc"):
                original_path = os.path.join(root, filename)
                normalized_name = normalize_filename(filename)
                match = best_match(normalized_name, reference_titles)

                if match:
                    safe_match = re.sub(r'[\/:*?\"<>|]', '-', match)
                    new_filename = f"{safe_match}.psarc"
                    new_path = os.path.join(root, new_filename)

                    if not os.path.exists(new_path):
                        os.rename(original_path, new_path)
                        log_entries.append(f"RENAMED: {original_path} -> {new_path}")
                    else:
                        log_entries.append(f"SKIPPED (duplicate): {original_path} -> {new_path}")
                else:
                    unmatched_path = os.path.join(UNMATCHED_FOLDER, filename)
                    shutil.move(original_path, unmatched_path)
                    log_entries.append(f"UNMATCHED: {original_path} -> moved to unmatched")

    with open(LOG_PATH, "w", encoding="utf-8") as log_file:
        log_file.write("\n".join(log_entries))

    print(f"Normalization complete. Log saved to {LOG_PATH}")

if __name__ == "__main__":
    normalize_cdlc()

