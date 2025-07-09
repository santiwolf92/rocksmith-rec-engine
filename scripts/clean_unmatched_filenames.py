import os
import re

# === SETTINGS ===
CDLC_FOLDER = r"C:\Program Files (x86)\Steam\steamapps\common\Rocksmith2014\dlc"
UNMATCHED_FOLDER = os.path.join(CDLC_FOLDER, "unmatched")

# Regex to remove common suffixes like _v1, _DD, _RS, etc.
suffix_pattern = re.compile(r'(_v\d+|_DD|_RS|_lead|_rhythm|_alt\d*|_combo|_part\d+)', re.IGNORECASE)

def clean_filename(filename):
    if not filename.endswith(".psarc"):
        return None

    base, ext = os.path.splitext(filename)

    # Handle trailing "_p"
    suffix = ""
    if base.endswith("_p"):
        base = base[:-2]
        suffix = "_p"

    # Remove known suffixes
    base = suffix_pattern.sub('', base)

    # Replace underscores with spaces
    base = base.replace('_', ' ')

    # Replace hyphens with spaces only in the artist name (before the first space or underscore)
    # If there's a hyphen near the start, it's probably part of the artist name
    parts = base.split(' ', 1)
    if len(parts) == 2:
        artist, song = parts
        artist = artist.replace('-', ' ')
        base = f"{artist} {song}"

    # Final formatting: Artist - Song_p.psarc
    parts = base.split(' ', 1)
    if len(parts) == 2:
        artist, song = parts
        new_name = f"{artist.strip()} - {song.strip()}{suffix}{ext}"
    else:
        new_name = f"{base.strip()}{suffix}{ext}"

    return new_name

# === PROCESS FILES IN "unmatched" ONLY ===
for file in os.listdir(UNMATCHED_FOLDER):
    full_path = os.path.join(UNMATCHED_FOLDER, file)
    if os.path.isfile(full_path):
        new_name = clean_filename(file)
        if new_name and new_name != file:
            new_path = os.path.join(UNMATCHED_FOLDER, new_name)
            print(f"Renaming:\n  {file}\n  -> {new_name}")
            os.rename(full_path, new_path)
