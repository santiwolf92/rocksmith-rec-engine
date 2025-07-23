import requests
import json

# Test data: Known CDLC that exists on CustomsForge
artist = "Led Zeppelin"
title = "Stairway to Heaven"

# Basic payload based on what we suspect the API expects
payload = {
    "columns[0][data]": "Title",
    "columns[1][data]": "Artist",
    "columns[2][data]": "Album",
    "columns[3][data]": "Tuning",
    "columns[4][data]": "Platform",
    "columns[5][data]": "SubmittedBy",
    "columns[6][data]": "Submitted",
    "columns[7][data]": "Rating",
    "columns[8][data]": "Version",
    "columns[9][data]": "Hits",
    "search[value]": f"{artist} {title}",
    "start": 0,
    "length": 10
}

try:
    response = requests.post("https://ignition4.customsforge.com/tablesettings", data=payload, timeout=10)
    if response.status_code == 200:
        print("✅ Successfully reached API!")
        data = response.json()
        results = data.get("data", [])
        print(f"Found {len(results)} results:")
        for result in results:
            print(f"- {result.get('Artist')} — {result.get('Title')}")
    else:
        print(f"❌ Status code: {response.status_code}")
except Exception as e:
    print(f"⚠️ Error during request: {e}")
