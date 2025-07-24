# scripts/cf_search.py

import requests
from urllib.parse import quote_plus
try:
    from cookies import cookies
except (ImportError, AttributeError):
    cookies = {}
    print("⚠️ Warning: No cookies loaded. Please paste them in the UI.")

def cdlc_exists_on_customsforge(artist, track):
    search_term = f"{artist} {track}"
    encoded_term = quote_plus(search_term.lower())

    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "en-GB,en;q=0.9,en-US;q=0.8,es;q=0.7",
        "referer": "https://ignition4.customsforge.com/",
        "x-requested-with": "XMLHttpRequest",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    }

    params = {
        "draw": "1",
        "start": "0",
        "length": "25",
        "search[value]": search_term,
        "filter_preferred_platform": "windows",
        "filter_hide_abandoned": "true",
    }

    url = "https://ignition4.customsforge.com/"
    try:
        response = requests.get(url, headers=headers, cookies=cookies, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json().get("data", [])
            for result in data:
                result_artist = str(result.get("Artist", "")).lower()
                result_title = str(result.get("Title", "")).lower()
                if artist.lower() in result_artist and track.lower() in result_title:
                    cdlc_id = result.get("id")
                    return f"https://ignition4.customsforge.com/cdlc/{cdlc_id}"
    except Exception as e:
        print(f"❌ CF search error for {artist} — {track}: {e}")

    return None
