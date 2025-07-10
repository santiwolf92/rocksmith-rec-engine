import os
import re
import csv
import git
from pathlib import Path

# === CONFIG ===
DLC_FOLDER = Path(r"F:/Rocksmith/dlc")
EXCLUDED_FOLDER = DLC_FOLDER / "01_CDLC Normalizer"
OUTPUT_CSV = Path(__file__).resolve().parent.parent / "data" / "cdlc_library.csv"
REPO_PATH = Path(__file__).resolve().parent.parent

# === PARSE ===
def parse_filename(filename):
    match = re.match(r"(.+?) - (.+?)_p\.psarc$", filename)
    if match:
        artist = match.group(1).strip()
        track = match.group(2).strip()
        return artist, track
    return None, None

# === WALK DLC FOLDER ===
def collect_cdlc():
    entries = []
    for root, dirs, files in os.walk(DLC_FOLDER):
        if EXCLUDED_FOLDER in map(Path, [root] + [os.path.join(root, d) for d in dirs]):
            continue
        for file in files:
            if file.lower().endswith("_p.psarc"):
                artist, track = parse_filename(file)
                if artist and track:
                    entries.append([artist, track, file])
    return entries

# === SAVE TO CSV ===
def save_to_csv(entries):
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Artist Name(s)", "Track Name", "file_name"])
        writer.writerows(entries)
    print(f"\n✅ Saved {len(entries)} entries to {OUTPUT_CSV}")

# === COMMIT TO GIT ===
def push_to_git():
    try:
        repo = git.Repo(REPO_PATH)
        repo.git.add(OUTPUT_CSV)
        if repo.is_dirty():
            repo.index.commit("Update CDLC library")
            origin = repo.remote(name='origin')
            origin.push()
            print("🚀 Pushed changes to GitHub")
        else:
            print("✅ No changes to commit")
    except Exception as e:
        print(f"⚠️ Git operation failed: {e}")

# === RUN ===
if __name__ == "__main__":
    cdlc_entries = collect_cdlc()
    save_to_csv(cdlc_entries)
    push_to_git()

