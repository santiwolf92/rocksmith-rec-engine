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

def clean_string(s):
    import string
    s = s.lower()
    s = s.translate(str.maketrans('', '', string.punctuation))
    s = re.sub(r'\s+', ' ', s)
    return s.strip()

def best_match(name, reference_titles):
    cleaned_reference = {clean_string(t): t for t in reference_titles}
    cleaned_input = clean_string(name)
    result = process.extractOne(cleaned_input, list(cleaned_reference.keys()), scorer=fuzz.token_sort_ratio)
    if result is None:
        return None
    match_key, score = result
    return cleaned_reference[match_key] if score >= 80 else None


# === MAIN LOGIC ===
def normalize_cdlc():
    OUTPUT_FOLDER = os.path.join(CDLC_FOLDER, "01_CDLC Normalizer")
    UNMATCHED_FOLDER = os.path.join(OUTPUT_FOLDER, "unmatched")
    LOG_PATH = os.path.join(OUTPUT_FOLDER, "rename_log.csv")

    os.makedirs(UNMATCHED_FOLDER, exist_ok=True)
    reference_titles = load_reference_titles()
    log_entries = []

    for root, _, files in os.walk(CDLC_FOLDER):
        # skip the output folder itself to avoid recursive renames
        if OUTPUT_FOLDER in root:
            continue

        for filename in files:
            if filename.lower().endswith(".psarc"):
                original_path = os.path.join(root, filename)
                normalized_name = normalize_filename(filename)
                match = best_match(normalized_name, reference_titles)

                if match:
                    safe_match = re.sub(r'[\\/:*?"<>|]', '-', match)
                    new_filename = f"{safe_match}_p.psarc"
                    new_path = os.path.join(root, new_filename)

                    if not os.path.exists(new_path):
                        os.rename(original_path, new_path)
                        log_entries.append(["RENAMED", original_path, new_path])
                    else:
                        log_entries.append(["SKIPPED (duplicate)", original_path, new_path])
                else:
                    unmatched_path = os.path.join(UNMATCHED_FOLDER, filename)
                    shutil.move(original_path, unmatched_path)
                    log_entries.append(["UNMATCHED", original_path, unmatched_path])

    df_log = pd.DataFrame(log_entries, columns=["Status", "Original Path", "New Path"])
    df_log.to_csv(LOG_PATH, index=False, encoding="utf-8")

    print(f"Normalization complete. Log saved to {LOG_PATH}")


if __name__ == "__main__":
    normalize_cdlc()

