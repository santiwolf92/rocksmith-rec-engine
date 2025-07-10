import os
import re
import pandas as pd
from pathlib import Path
import subprocess

DLC_FOLDER = Path(r"C:\Program Files (x86)\Steam\steamapps\common\Rocksmith2014\dlc")
OUTPUT_CSV = Path(__file__).resolve().parent.parent / "data" / "cdlc_library.csv"
EXCLUDED_DIRS = {"01_CDLC Normalizer"}

def parse_psarc_filename(filename):
    base = filename.replace("_p.psarc", "").replace(".psarc", "")
    base = re.sub(r'(?i)(\bv\d+(\.\d+)*\b|rs2014|remastered|deluxe|explicit|version|lead|rhythm|combo|alt\d*|part\d+)', '', base)
    base = re.sub(r'[-_.]+', ' ', base)
    base = re.sub(r'\s+', ' ', base).strip().title()
    return base

def extract_metadata(base_name):
    if ' - ' in base_name:
        parts = base_name.split(' - ', 1)
    elif '_' in base_name:
        parts = base_name.split('_', 1)
    else:
        parts = base_name.split(None, 1)

    if len(parts) == 2:
        artist, track = parts
    else:
        artist, track = "Unknown", parts[0]
    return artist.strip(), track.strip()

def scan_dlc_folder():
    entries = []
    for root, dirs, files in os.walk(DLC_FOLDER):
        # Skip excluded directories
        if any(excluded in root for excluded in EXCLUDED_DIRS):
            continue

        for file in files:
            if file.lower().endswith(".psarc"):
                file_path = Path(root) / file
                base_name = parse_psarc_filename(file)
                artist, track = extract_metadata(base_name)
                entries.append({
                    "Artist Name(s)": artist,
                    "Track Name": track,
                    "file_name": file
                })
    return entries

def update_library():
    entries = scan_dlc_folder()
    print(f"✅ Found {len(entries)} valid .psarc entries")

    if not entries:
        print("⚠️ No files found. Aborting update to avoid data loss.")
        return

    df = pd.DataFrame(entries)
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"✅ Saved {len(df)} entries to {OUTPUT_CSV}")

    try:
        subprocess.run(["git", "add", str(OUTPUT_CSV)], check=True)
        subprocess.run(["git", "commit", "-m", "Update CDLC library"], check=True)
        subprocess.run(["git", "push"], check=True)
        print("🚀 Pushed changes to GitHub")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Git operation failed: {e}")

if __name__ == "__main__":
    update_library()

