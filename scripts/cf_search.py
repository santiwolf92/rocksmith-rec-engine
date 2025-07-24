# scripts/cf_search.py

import requests
from urllib.parse import quote_plus
try:
    from cookies import cookies
except (ImportError, AttributeError):
    cookies = {}
    print("⚠️ Warning: No cookies loaded. Please paste them in the UI.")

def cdlc_exists_on_customsforge(artist, track):
    from cookies import cookies
    import requests
    from urllib.parse import quote_plus

    query = f"{artist} {track}"
    encoded_query = quote_plus(query)
    url = "https://ignition4.customsforge.com/"
    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "referer": "https://ignition4.customsforge.com/",
        "x-requested-with": "XMLHttpRequest",
        "user-agent": "Mozilla/5.0",
    }

    params = {
        "draw": "1",
        "start": "0",
        "length": "25",
        "search[value]": query,
        "filter_preferred_platform": "windows",
        "filter_hide_abandoned": "true",
    }

    try:
        response = requests.get(url, headers=headers, cookies=cookies, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        for result in data.get("data", []):
            try:
                result_artist = str(result.get("Artist", "")).lower()
                result_title = str(result.get("Title", "")).lower()
            except Exception as e:
                print(f"⚠️ Error parsing result: {e}")
                continue
            if artist.lower() in result_artist and track.lower() in result_title:
                cdlc_id = result.get("id")
                return f"https://ignition4.customsforge.com/cdlc/{cdlc_id}"
    except Exception as e:
        print(f"⚠️ Error searching for {artist} - {track}: {e}")

    return None
