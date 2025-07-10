import os
import csv
import re
import subprocess
from pathlib import Path

DLC_FOLDER = Path(r"F:\Rocksmith\dlc")
EXCLUDED_FOLDER = DLC_FOLDER / "01_CDLC Normalizer"
OUTPUT_CSV = Path(__file__).resolve().parent.parent / "data" / "cdlc_library.csv"

def parse_filename(file_name):
    # Expecting: "Artist Name(s) - Track Name_p.psarc"
    name = file_name.replace("_p.psarc", "").strip()
    if " - " in name:
        artist, track = name.split(" - ", 1)
        return artist.strip(), track.strip()
    return None, None

def collect_cdlc_entries():
    entries = []
    for root, dirs, files in os.walk(DLC_FOLDER):
        if EXCLUDED_FOLDER in Path(root).parents or Path(root) == EXCLUDED_FOLDER:
            continue
        for file in files:
            if file.lower().endswith("_p.psarc"):
                artist, track = parse_filename(file)
                if artist and track:
                    entries.append([artist, track, file])
    return entries

def save_to_csv(entries):
    OUTPUT_CSV.parent.mkdir(exist_ok=True)
    with open(OUTPUT_CSV, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Artist Name(s)", "Track Name", "file_name"])
        writer.writerows(entries)
    print(f"\nSaved {len(entries)} entries to {OUTPUT_CSV}")

def push_to_git():
    def push_to_git():
    repo_dir = Path(__file__).resolve().parent.parent  # go up to project root

        try:
            subprocess.run(["git", "add", str(OUTPUT_CSV)], check=True, cwd=repo_dir)
            subprocess.run(["git", "commit", "-m", "Update CDLC library"], check=True, cwd=repo_dir)
            subprocess.run(["git", "push"], check=True, cwd=repo_dir)
        except subprocess.CalledProcessError as e:
            print("Git operation failed:", e)

if __name__ == "__main__":
    cdlc_entries = collect_cdlc_entries()
    save_to_csv(cdlc_entries)
    push_to_git()

