import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

# === CONFIGURATION ===
SEARCH_TERM = "Stairway to Heaven"
ENCODED_TERM = quote_plus(SEARCH_TERM.lower())

# === HEADERS & COOKIES ===
headers = {
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-language": "en-GB,en;q=0.9,en-US;q=0.8,es;q=0.7",
    "referer": "https://ignition4.customsforge.com/",
    "x-requested-with": "XMLHttpRequest",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0",
}

cookies = {
    # Your cookies go here
    "ips4_device_key": "645bd0b959cd970cd1075abf409b8d00",
    "ips4_forum_view": "table",
    "__eoi": "ID=0348d2efe62a6935:T=1738090324:RT=1738174489:S=AA-AfjZsCqcPCcQ0w3woMKhlIiYa",
    "ips4_cookie_consent": "1",
    "ips4_cookie_consent_optional": "1",
    "ips4_member_id": "512899",
    "ips4_login_key": "ec8240b88746352dd69ed968049f03de",
    "ips4_IPSSessionFront": "d63e881b49b4a25c2749f81f7e654373",
    "ips4_loggedIn": "1753306833",
    "XSRF-TOKEN": "eyJpdiI6IkhOT...<truncated>",
    "ignition4_session": "eyJpdiI6IlNhZ...<truncated>",
    "remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d": "eyJpdiI6InB4c1...<truncated>"
}

# === REQUEST ===
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

    try:
        json_data = response.json()
        print(f"✅ Found {len(json_data.get('data', []))} results:\n")

        for entry in json_data.get("data", []):
            html = entry.get("DT_RowData", {}).get("content", "")
            soup = BeautifulSoup(html, "html.parser")

            artist_tag = soup.find("span", class_="table-link truncate")
            title_tag = soup.find("a", class_="table-link", href=lambda x: x and "/cdlc/" in x)
            link_tag = soup.find_all("a")[-1]  # last <a> is usually the external download link

            artist = artist_tag.text.strip() if artist_tag else ""
            title = title_tag.text.strip() if title_tag else ""
            link = link_tag["href"].strip() if link_tag else ""

            # Skip if artist and title are both missing
            if not artist and not title:
                continue

            print(f"🎵 {artist} — {title}")
            print(f"🔗 {link}\n")

    except Exception:
        print("⚠️ Could not parse response as JSON")
        print(response.text[:800])  # Show preview of HTML for debugging

except requests.exceptions.RequestException as e:
    print(f"❌ Request failed: {e}")

