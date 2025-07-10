import os
import csv
import re
from pathlib import Path
import subprocess

# === CONFIGURATION ===
DLF_PATH = Path(r"F:/SteamLibrary/steamapps/common/Rocksmith2014/dlc")
EXCLUDE_FOLDER = DLF_PATH / "01_CDLC Normalizer"
OUTPUT_CSV = Path(__file__).resolve().parent.parent / "data" / "cdlc_library.csv"

# === HELPERS ===
def parse_filename(filename):
    name = filename.replace("_p.psarc", "").replace(".psarc", "")
    name = re.sub(r"[_]+", " ", name)  # underscores to space
    name = re.sub(r"(?i)\b(v|ver|rs2014|remastered|explicit|deluxe|lead|rhythm|combo|alt|part)\d*(\.\d+)*\b", "", name)
    name = re.sub(r"[\[\](){}]", "", name)
    name = re.sub(r"\s+", " ", name).strip()

    if " - " in name:
        artist, track = name.split(" - ", 1)
    else:
        parts = name.split(" ")
        artist = parts[0]
        track = " ".join(parts[1:])

    return artist.strip().title(), track.strip().title()

# === MAIN ===
def collect_psarcs():
    all_entries = []
    for root, dirs, files in os.walk(DLF_PATH):
        if EXCLUDE_FOLDER in Path(root).parents or Path(root) == EXCLUDE_FOLDER:
            continue
        for file in files:
            if file.lower().endswith(".psarc"):
                full_path = Path(root) / file
                artist, track = parse_filename(file)
                all_entries.append([artist, track, file])
    return all_entries

def save_to_csv(entries):
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_CSV, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Artist Name(s)", "Track Name", "file_name"])
        writer.writerows(entries)
    print(f"✅ Saved {len(entries)} entries to {OUTPUT_CSV}")

def push_to_git():
    try:
        subprocess.run(["git", "add", str(OUTPUT_CSV)], check=True)
        subprocess.run(["git", "commit", "-m", "Update CDLC library"], check=True)
        subprocess.run(["git", "push"], check=True)
        print("🚀 Pushed changes to GitHub")
    except subprocess.CalledProcessError as e:
        print("⚠️ Git operation failed:", e)

if __name__ == "__main__":
    entries = collect_psarcs()
    save_to_csv(entries)
    push_to_git()

