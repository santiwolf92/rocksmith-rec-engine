import os
import re
import csv
import subprocess

# === PATHS ===
DLC_FOLDER = r"C:\Program Files (x86)\Steam\steamapps\common\Rocksmith2014\dlc"
EXCLUDED_DIRS = {"01_CDLC Normalizer"}
OUTPUT_CSV = r"F:\rocksmith-rec-engine\data\cdlc_library.csv"
REPO_DIR = r"F:\rocksmith-rec-engine"

# === NORMALIZATION ===
def normalize_filename(filename):
    base = re.sub(r'_p\.psarc$', '', filename, flags=re.IGNORECASE)
    base = re.sub(
        r'(?i)(\bv\d+(\.\d+)*\b|rs2014|remastered|deluxe|explicit|version|lead|rhythm|combo|alt\d*|part\d+)',
        '',
        base
    )
    base = re.sub(r'[-_.]+', ' ', base)
    return re.sub(r'\s+', ' ', base).strip().title()

# === MAIN SCRIPT ===
def update_cdlc_library():
    entries = []

    for root, dirs, files in os.walk(DLC_FOLDER):
        if any(excluded in root for excluded in EXCLUDED_DIRS):
            continue

        for file in files:
            if file.endswith(".psarc"):
                clean_name = normalize_filename(file)
                parts = clean_name.split(" ", 1)
                if len(parts) < 2:
                    continue
                artist, title = parts
                entries.append([artist.strip(), title.strip(), file])

    with open(OUTPUT_CSV, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Artist Name(s)", "Track Name", "file_name"])
        writer.writerows(entries)

    print(f"✅ Saved {len(entries)} entries to {OUTPUT_CSV}")

    # === Git Commit and Push ===
    try:
        subprocess.run(["git", "add", OUTPUT_CSV], cwd=REPO_DIR, check=True)
        subprocess.run(["git", "commit", "-m", "Update CDLC library"], cwd=REPO_DIR, check=True)
        subprocess.run(["git", "push"], cwd=REPO_DIR, check=True)
        print("🚀 Pushed changes to GitHub")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Git operation failed: {e}")

if __name__ == "__main__":
    update_cdlc_library()

