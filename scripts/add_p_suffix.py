import os

FOLDER = r"C:\Program Files (x86)\Steam\steamapps\common\Rocksmith2014\dlc"

for root, _, files in os.walk(FOLDER):
    for filename in files:
        if filename.lower().endswith(".psarc") and not filename.lower().endswith("_p.psarc"):
            base = filename[:-6]  # remove '.psarc'
            new_filename = f"{base}_p.psarc"
            old_path = os.path.join(root, filename)
            new_path = os.path.join(root, new_filename)
            os.rename(old_path, new_path)
            print(f"Renamed: {filename} -> {new_filename}")

print("Done.")
