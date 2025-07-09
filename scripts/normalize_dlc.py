import os
import re
import pandas as pd
from fuzzywuzzy import process, fuzz

# === PATHS ===
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FOLDER = os.path.join(PROJECT_ROOT, "data")
UNMATCHED_FOLDER = r"C:\Program Files (x86)\Steam\steamapps\common\Rocksmith2014\dlc\01_CDLC Normalizer\unmatched"
LOG_PATH = os.path.join(UNMATCHED_FOLDER, "rename_log.csv")

HISTORY_FILES = [
    os.path.join(DATA_FOLDER, "lastfm_history.csv"),
    os.path.join(DATA_FOLDER, "spotify_liked.csv"),
]

# === LOAD LISTENING HISTORY ===
def load_reference_titles():
    titles = set()
    for path in HISTORY_FILES:
        print(f"Checking: {path}")
        if os.path.exists(path):
            print(f" → Found: {path}")
            df = pd.read_csv(path)
            print(f" → Columns: {list(df.columns)}")

            if 'Artist Name(s)' in df.columns and 'Track Name' in df.columns:
                df = df.rename(columns={'Artist Name(s)': 'artist', 'Track Name': 'track'})
            elif 'artist_name' in df.columns and 'track_name' in df.columns:
                df = df.rename(columns={'artist_name': 'artist', 'track_name': 'track'})
            else:
                print(" → Column names did not match expected formats.")
                continue

            print(f" → Rows loaded: {len(df)}")

            for artist, track in zip(df['artist'], df['track']):
                full_title = f"{artist.strip()} - {track.strip()}"

                # Remove fluff from track name
                full_title = re.sub(r'(?i)\s*\((remastered|deluxe|explicit|version.*?)\)', '', full_title)
                full_title = re.sub(r'(?i)\s*-\s*(remastered|deluxe|explicit|version.*?)$', '', full_title)
                full_title = full_title.strip()

                titles.add(full_title)

        else:
            print(f" → NOT FOUND: {path}")

    print(f"\nLoaded {len(titles)} reference titles:")
    for title in sorted(titles)[:20]:  # Print first 20
        print("-", title)

    return titles

# === FILENAME NORMALIZATION ===
def normalize_filename(filename):
    base = re.sub(r'_p\.psarc$', '', filename, flags=re.IGNORECASE)

    # Remove version tags and suffixes like v1, v1.2, RS2014, remastered, etc.
    base = re.sub(
        r'(?i)(\bv\d+(\.\d+)*\b|RS2014|DD|remastered|deluxe|explicit|lead|rhythm|combo|alt\d*|part\d+)',
        '',
        base
    )

    # Replace separators with space
    base = re.sub(r'[-_.]+', ' ', base)

    # Remove known junk words
    base = re.sub(r'(?i)\b(rs2014|remastered|deluxe|explicit|v\d+(\.\d+)*|psarc)\b', '', base)

    # Collapse multiple spaces
    base = re.sub(r'\s+', ' ', base)

    return base.strip().title()

# === CLEAN STRING FOR MATCHING ===
def clean_string(s):
    import string
    s = s.lower()
    s = s.translate(str.maketrans('', '', string.punctuation))
    s = re.sub(r'\s+', ' ', s)
    return s.strip()

# === FUZZY MATCH ===
def best_match(name, reference_titles):
    cleaned_reference = {clean_string(t): t for t in reference_titles}
    cleaned_input = clean_string(name)
    result = process.extractOne(cleaned_input, list(cleaned_reference.keys()), scorer=fuzz.token_sort_ratio)
    if result is None:
        return None
    match_key, score = result
    print(f" → Matching '{cleaned_input}' to '{match_key}' (score: {score})")
    return cleaned_reference[match_key] if score >= 80 else None

# === MAIN SCRIPT ===
def normalize_unmatched():
    reference_titles = load_reference_titles()
    log_entries = []

    for filename in os.listdir(UNMATCHED_FOLDER):
        if not filename.lower().endswith(".psarc"):
            continue

        original_path = os.path.join(UNMATCHED_FOLDER, filename)
        normalized_name = normalize_filename(filename)
        print(f"\nProcessing: {filename} → {normalized_name}")
        match = best_match(normalized_name, reference_titles)

        if match:
            # Sanitize and format the match string
            safe_match = re.sub(r'[\/:*?"<>|]', '-', match)
            if not safe_match.lower().endswith('_p'):
                safe_match += '_p'

            new_filename = f"{safe_match}.psarc"
            new_path = os.path.join(UNMATCHED_FOLDER, new_filename)

            if not os.path.exists(new_path):
                os.rename(original_path, new_path)
                log_entries.append(["RENAMED", filename, new_filename])
            else:
                log_entries.append(["SKIPPED (duplicate)", filename, new_filename])
        else:
            log_entries.append(["NO MATCH", filename, ""])

    # Save log
    df_log = pd.DataFrame(log_entries, columns=["Status", "Original Filename", "New Filename"])
    df_log.to_csv(LOG_PATH, index=False, encoding="utf-8")
    print(f"\nDone. Log saved to: {LOG_PATH}")

if __name__ == "__main__":
    normalize_unmatched()


