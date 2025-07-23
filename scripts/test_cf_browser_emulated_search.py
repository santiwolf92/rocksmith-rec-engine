import requests
from urllib.parse import quote_plus

# === USER CREDENTIALS ===
email = "santilobo123@gmail.com"  # <- replace
password = "Simba0562_Customsforge"   # <- replace

# === SEARCH CONFIGURATION ===
search_term = "Stairway to Heaven"
encoded_term = quote_plus(search_term.lower())

# === START SESSION ===
session = requests.Session()
login_url = "https://www.customsforge.com/login/"

session.headers.update({
    "User-Agent": "Mozilla/5.0",
    "Referer": login_url,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
})

login_payload = {
    "auth": email,
    "password": password,
    "rememberMe": "1"
}

print(f"🔐 Logging in as {email}...")
login_response = session.post(login_url, data=login_payload)
if "Sign Out" in login_response.text or login_response.url != login_url:
    print("✅ Login successful!")

    # Search request
    search_url = "https://ignition4.customsforge.com/"
    params = {
        "draw": "1",
        "start": "0",
        "length": "25",
        "search[value]": search_term,
        "filter_preferred_platform": "windows",
        "filter_hide_abandoned": "true",
    }

    print(f"🔎 Searching for: {search_term}")
    response = session.get(search_url, params=params)
    print(f"🔎 Status: {response.status_code}")

    try:
        data = response.json().get("data", [])
        print(f"✅ Found {len(data)} results:\n")
        for entry in data:
            artist = entry.get("artistName", "Unknown")
            title = entry.get("title", "Unknown")
            url = f"https://ignition4.customsforge.com/cdlc/{entry.get('id')}"
            print(f"🎵 {artist} — {title}\n🔗 {url}\n")
    except Exception:
        print("⚠️ Could not parse response as JSON")
        print(response.text[:800])
else:
    print("❌ Login failed. Check your credentials.")
