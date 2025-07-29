# scripts/cf_search.py

import requests
from urllib.parse import quote_plus
from difflib import SequenceMatcher
import re

try:
    from cookies import cookies
except (ImportError, AttributeError):
    cookies = {}
    print("⚠️ Warning: No cookies loaded. Please paste them in the UI.")

def normalize_title(title):
    title = re.sub(r'[\(\[\{].*?[\)\]\}]', '', title)
    title = re.sub(r'[-–—]\s*(live|acoustic|remaster(ed)?|version.*|mono|stereo).*$', '', title, flags=re.I)
    return title.strip().lower()

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def cdlc_exists_on_customsforge(artist, track):
    search_term = f"{artist} {track}"
    encoded_term = quote_plus(search_term)

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
        response = requests.get(url, headers=headers, cookies=cookies, params=params, timeout=20)
        if response.status_code == 200:
            data = response.json().get("data", [])
            if data:
                first_result = data[0]
                print(f"🔍 First CF result raw data: {first_result}")  # << Debug print

                result_title = first_result.get("Title", "").strip()

                query_title = normalize_title(track)
                matched_title = normalize_title(result_title)
                similarity = similar(matched_title, query_title)

                if similarity >= 0.70:
                    cdlc_id = first_result.get("id")
                    if cdlc_id:
                        return f"https://ignition4.customsforge.com/cdlc/{cdlc_id}"
                elif similarity < 0.50:
                    print(f"❌ Likely mismatch: searched '{track}', got '{result_title}' (sim={similarity:.2f})")
                else:
                    print(f"⚠️ Borderline match: searched '{track}', got '{result_title}' (sim={similarity:.2f})")

            return False
        else:
            print(f"⚠️ CF search failed with status {response.status_code} for: {artist} — {track}")
            return False
    except Exception as e:
        print(f"❌ CF search error for {artist} — {track}: {e}")
        return False
