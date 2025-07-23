import requests
from bs4 import BeautifulSoup

# === SEARCH TERM ===
search_query = "Stairway to Heaven"

# === HEADERS & COOKIES ===
headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "https://ignition4.customsforge.com/",
}

cookies = {
    "ips4_device_key": "645bd0b959cd970cd1075abf409b8d00",
    "ips4_forum_view": "table",
    "__eoi": "ID=0348d2efe62a6935:T=1738090324:RT=1738174489:S=AA-AfjZsCqcPCcQ0w3woMKhlIiYa",
    "ips4_cookie_consent": "1",
    "ips4_cookie_consent_optional": "1",
    "ips4_member_id": "512899",
    "ips4_login_key": "ec8240b88746352dd69ed968049f03de",
    "ips4_IPSSessionFront": "d63e881b49b4a25c2749f81f7e654373",
    "ips4_loggedIn": "1753309262",
    "XSRF-TOKEN": "eyJpdiI6ImRGSnJPVFRackRKM2VXNEcxcURyUnc9PSIsInZhbHVlIjoiWDVia1c5Q2YweEpXems0M1Y5OWpTMWxnUWg2U1pDK2RUR29ybzJndUI0OFJ3UjF6NFZtSXhwTUZnbmdZRElWQTVWOW83TnNjUjJkRm5vdTVkY2RVcHNEMy9lUmJDcGNsTlJYRGRld2E5ME9Gd09lTGcyTHgwdnlSbXNsTFM1cm8iLCJtYWMiOiJiMjBjMTk5MjgyMzdiMWVkN2E1YjUyYmU5OTIxNTM4MTQ3ZmQyYzZmYTJjYzJmMDU1YjM1MmQ2ZWZmZDg5M2YzIiwidGFnIjoiIn0=",
    "ignition4_session": "eyJpdiI6IjdCZ3dLZkUvMkUyK1VkZFRkbCszNEE9PSIsInZhbHVlIjoibFlBRmRwaVo0MXdyaWtqeVBxRnlDeU9kaFlPOFdKUkdMeThNeC95TCsvMXd1YzNlTlViOFNmK2lqR3BVNVl0TlpnWlgrK0I5Z2M5bGtCZTJndXVvL2xydi9BNVg2YVZuRmUvaTJVaTA5MlhCbE1qekIzV044T25qOGdZa1pRUXciLCJtYWMiOiJjNjk4MWM4MDY5ODAyMzU4ZDhkNWQ2NmZjMzRmN2FiOGZjY2I4MmU4ZmJhYzc1YzU5MThiMzgyNzAwMGQ0OTE1IiwidGFnIjoiIn0=",
    "remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d": "eyJpdiI6ImpGeWVOZ3hObXB1R2psQnFBbEp3aHc9PSIsInZhbHVlIjoiNnVmZ09PMkpIWjJzN2V4cjdyTWJrVDlVREVkZFhQWUpHN3FUZmN6MmkxcjJKNSs2ajNpYVN6YzdTR1JCQnpFSkNBa0tlcWUrdTdWcEZqUVcyQTlQbUI2a0hvb09YUDBPS2pnNUw1K0JQWDNpdFpHSlJFNTFxMDRtbS9YRTFLcE4zb0pXeFJzbjdsblRaZlNoaFdvVEhnPT0iLCJtYWMiOiJlYzk0MTc2MjdhOGRhNTNmOTNjMzE2MDBiZjM1ZGI1YTQ3MzFiYWQ1ZDIzNjhmMzI2YjNiMTVmYzA3MjNhNWYyIiwidGFnIjoiIn0=",
}

# === DO THE REQUEST ===
url = f"https://ignition4.customsforge.com/search/{search_query.replace(' ', '%20')}"

print(f"🔎 Searching for: {search_query}")
response = requests.get(url, headers=headers, cookies=cookies)
print(f"🔎 Status: {response.status_code}")

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.select("a.table-link[href*='/cdlc/']")
    if not results:
        print("❌ No results found.")
    else:
        print(f"✅ Found {len(results)} results:")
        for r in results:
            artist_elem = r.find_previous("span", class_="table-link")
            artist = artist_elem.text.strip() if artist_elem else "Unknown Artist"
            title = r.text.strip()
            link = r['href']
            print(f"🎵 {artist} — {title}\n   🔗 {link}")
else:
    print("❌ Failed to get a valid response.")

