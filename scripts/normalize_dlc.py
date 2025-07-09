import os
import re
import pandas as pd
from fuzzywuzzy import process, fuzz

# === PATHS ===
UNMATCHED_FOLDER = r"C:\Program Files (x86)\Steam\steamapps\common\Rocksmith2014\dlc\unmatched"
LOG_PATH = os.path.join(UNMATCHED_FOLDER, "rename_log.csv")

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

# === FILENAME NORMALIZATION ===
def normalize_filename(filename):
    base = re.sub(r'_p\.psarc$', '', filename, flags=re.IGNORECASE)

    # Remove common suffixes: v1, v2.1, DD, RS, etc.
    base = re.sub(r'(\bv\d+(\.\d+)?\b|_?DD\b|_?RS\b|_?lead|_?rhythm|_?combo|_?alt\d*|_?part\d+)', '', base, flags=re.IGNORECASE)

    # Replace separators with space
    base = re.sub(r'[-_.]+', ' ', base)

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
    print(f"Done. Log saved to: {LOG_PATH}")

if __name__ == "__main__":
    normalize_unmatched()

