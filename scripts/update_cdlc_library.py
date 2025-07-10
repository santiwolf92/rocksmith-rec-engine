import os
import re
import pandas as pd
from pathlib import Path
import subprocess

# === PATHS ===
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_FOLDER = PROJECT_ROOT / "data"
CDLC_CSV_PATH = DATA_FOLDER / "cdlc_library.csv"
DLF_FOLDER = Path(r"F:\Rocksmith2014\dlc")

# === PARSE FILENAME ===
def parse_filename(filename):
    name = filename.replace("_p", "").replace(".psarc", "")
    name = re.sub(r'[_\-]', ' ', name)
    name = re.sub(r'(?i)\bv\d+(\.\d+)*\b|rs2014|remastered|deluxe|explicit|version|lead|rhythm|combo|alt\d*|part\d+', '', name)
    name = re.sub(r'\s+', ' ', name).strip().title()

    if " - " in name:
        parts = name.split(" - ", 1)
    elif " " in name:
        parts = name.split(" ", 1)
    else:
        parts = [name, ""]

    artist = parts[0].strip()
    track = parts[1].strip() if len(parts) > 1 else ""
    return artist, track

# === MAIN SCRIPT ===
def build_cdlc_library():
    entries = []

    for root, dirs, files in os.walk(DLF_FOLDER):
        if "01_CDLC Normalizer" in root:
            continue
        for file in files:
            if file.lower().endswith(".psarc"):
                artist, track = parse_filename(file)
                entries.append({
                    "Artist Name(s)": artist,
                    "Track Name": track,
                    "file_name": file
                })

    df = pd.DataFrame(entries)
    df.to_csv(CDLC_CSV_PATH, index=False, encoding="utf-8")
    print(f"✅ Saved {len(df)} entries to {CDLC_CSV_PATH}")
    return True

# === GIT PUSH ===
def git_push():
    try:
        subprocess.run(["git", "add", str(CDLC_CSV_PATH)], cwd=str(PROJECT_ROOT), check=True)
        subprocess.run(["git", "commit", "-m", "Update CDLC library"], cwd=str(PROJECT_ROOT), check=True)
        subprocess.run(["git", "push"], cwd=str(PROJECT_ROOT), check=True)
        print("🚀 Pushed changes to GitHub")
    except subprocess.CalledProcessError as e:
        print("⚠️ Git operation failed:", e)

# === RUN ===
if __name__ == "__main__":
    if build_cdlc_library():
        git_push()
