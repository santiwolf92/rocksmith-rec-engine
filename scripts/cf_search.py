import requests
from urllib.parse import quote_plus
from cookies import cookies  # ✅ Load from external file

# === CONFIGURATION ===
SEARCH_TERM = "Black Sabbath Paranoid"
ENCODED_TERM = quote_plus(SEARCH_TERM.lower())

# === HEADERS ===
headers = {
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-language": "en-GB,en;q=0.9,en-US;q=0.8,es;q=0.7",
    "referer": "https://ignition4.customsforge.com/",
    "x-requested-with": "XMLHttpRequest",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0",
}

# === SEARCH PARAMETERS ===
params = {
    "draw": "1",
    "start": "0",
    "length": "25",
    "search[value]": SEARCH_TERM,
    "filter_preferred_platform": "windows",
    "filter_hide_abandoned": "true",
}

url = "https://ignition4.customsforge.com/"
print(f"🔎 Searching for: {SEARCH_TERM}")

try:
    response = requests.get(url, headers=headers, cookies=cookies, params=params)
    print(f"🔎 Status: {response.status_code}")

    json_data = response.json()
    results = json_data.get("data", [])

    print(f"✅ Found {len(results)} results:\n")

    artist_map = {
        33: "Led Zeppelin",
        810: "Rodrigo y Gabriela",
        8875: "Led Zeppelin/Igor Presnyakov",
        # Expand as needed
    }

    for entry in results:
        title = entry.get("title", "Unknown Title")
        artist_id = entry.get("artist_id")
        artist = artist_map.get(artist_id, f"[Artist ID {artist_id}]")
        cdlc_id = entry.get("id")
        cdlc_url = f"https://ignition4.customsforge.com/cdlc/{cdlc_id}"

        print(f"🎵 {artist} — {title}")
        print(f"🔗 {cdlc_url}\n")

except Exception as e:
    print(f"❌ Error: {e}")
