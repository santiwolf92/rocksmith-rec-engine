import os

# Folder to create test files in
UNMATCHED_FOLDER = r"C:\Program Files (x86)\Steam\steamapps\common\Rocksmith2014\dlc\01_CDLC Normalizer\unmatched"

# Some intentionally messy examples
dummy_filenames = [
    "Red-Hot-Chili-Peppers_So-Much-I_v1.2_DD_p.psarc",
    "The.Strokes-Reptilia_v2_RS.psarc",
    "Queen_Bohemian-Rhapsody_v1_lead.psarc",
    "Led.Zeppelin-Stairway_To_Heaven_alt1_p.psarc",
    "Arctic_Monkeys-Do_I_Wanna_Know_v3.1_combo.psarc",
    "RadioheadLuckyv1.0RS2014.psarc",
    "Radiohead-Idioteque_v1.0_RS2014.psarc",

]

for name in dummy_filenames:
    path = os.path.join(UNMATCHED_FOLDER, name)
    with open(path, 'w') as f:
        f.write("dummy data")  # fake content for testing

print("Dummy test files created.")
