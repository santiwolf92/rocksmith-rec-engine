import requests
from bs4 import BeautifulSoup

SEARCH_TERM = "Stairway to Heaven"

# Paste your updated browser cookies here
COOKIES = {
    "ips4_device_key": "645bd0b959cd970cd1075abf409b8d00",
    "ips4_member_id": "512899",
    "ips4_login_key": "ec8240b88746352dd69ed968049f03de",
    "ips4_IPSSessionFront": "d63e881b49b4a25c2749f81f7e654373",
    "ips4_loggedIn": "1753306833",
    "ignition4_session": "eyJpdiI6IlNhZllXTzNzTzgxdkJ2Wnl2ak1YVkE9PSIsInZhbHVlIjoiS1lGejVlYlRFdlhpNk9MVjcvdVh6aGJKMExaQXVSTXdSSGgzd0RZTGd2TzZxNkxVUFpiTW9MOUdJbTl3L1FOcVVlREhIQ1NZOHlRKzY0QjdMU082QXAzaXNiNzBLQWhKaWRIenpTUXg1QlJrNTNPSXdsNW0xTy85WGNLSklTZzIiLCJtYWMiOiI3NDc5NmY5ZDViNzViY2M4YjE5NTY0MzViNjJhNDY0NDBkMmE1YjEwMTAzZGNiYzI4NGE4YTI4ZDg2NGI1MDIzIiwidGFnIjoiIn0%3D",
    # ... add any others needed
}

headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://ignition4.customsforge.com/",
}

params = {
    "search": SEARCH_TERM,
}

print(f"🔎 Searching for: {SEARCH_TERM}")
response = requests.get(
    "https://ignition4.customsforge.com/search",
    headers=headers,
    cookies=COOKIES,
    params=params,
)

print(f"🔎 Status: {response.status_code}")
if response.status_code != 200:
    print("❌ Failed to get a valid response.")
    exit()

soup = BeautifulSoup(response.text, "html.parser")
results = []

# Find each row in the search table
for row in soup.select("tbody tr"):
    try:
        artist = row.select_one("td:nth-of-type(2)").get_text(strip=True)
        title = row.select_one("td:nth-of-type(3) a.table-link").get_text(strip=True)
        url = row.select_one("td:nth-of-type(3) a.table-link")["href"]
        if not url.startswith("http"):
            url = "https://ignition4.customsforge.com" + url
        results.append({"artist": artist, "title": title, "url": url})
    except Exception:
        continue

print(f"✅ Found {len(results)} results:")
for item in results:
    print(f"🎵 {item['artist']} — {item['title']}\n🔗 {item['url']}")


