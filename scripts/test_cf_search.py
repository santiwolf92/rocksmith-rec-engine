import requests
import json

url = "https://ignition4.customsforge.com/"

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
    "search[value]": "Stairway to Heaven",
    "start": 0,
    "length": 5,
    "draw": 3,
}

headers = {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
}

response = requests.post(url, data=payload, headers=headers)

if response.status_code == 200:
    print("✅ Success!")
    data = response.json()
    results = data.get("data", [])
    for i, result in enumerate(results, 1):
        artist = result.get("artist", "Unknown Artist")
        title = result.get("title", "Unknown Title")
        downloads = result.get("downloads", 0)
        print(f"{i}. {artist} — {title} ({downloads} downloads)")
else:
    print(f"❌ Status Code: {response.status_code}")
    print(response.text)
