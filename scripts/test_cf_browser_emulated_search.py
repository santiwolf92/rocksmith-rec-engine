import requests
from urllib.parse import quote_plus

# === CONFIG ===
SEARCH_TERM = "stairway to heaven"

HEADERS = {
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-language": "en-GB,en;q=0.9,en-US;q=0.8,es;q=0.7",
    "referer": "https://ignition4.customsforge.com/",
    "x-requested-with": "XMLHttpRequest",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin"
}

COOKIES = {
    "ips4_device_key": "645bd0b959cd970cd1075abf409b8d00",
    "ips4_forum_view": "table",
    "__eoi": "ID=0348d2efe62a6935:T=1738090324:RT=1738174489:S=AA-AfjZsCqcPCcQ0w3woMKhlIiYa",
    "ips4_cookie_consent": "1",
    "ips4_cookie_consent_optional": "1",
    "ips4_member_id": "512899",
    "ips4_login_key": "ec8240b88746352dd69ed968049f03de",
    "ips4_IPSSessionFront": "d63e881b49b4a25c2749f81f7e654373",
    "ips4_loggedIn": "1753304006",
    "XSRF-TOKEN": "eyJpdiI6ImErL2JEOFl1elJ1M0VJU3drdkdtTkE9PSIsInZhbHVlIjoicXBTdUNROHJLTC80bFNZWGJtZTliMEVka0k3UkRBdkhleWVuM29IalBjdkg4UCsrYWRiTHRDNktQQ1FqSDRIMjNvTVJrWVA4RHd6Y0V3U2grTHNkbFA0Tm1tRXJhRndKNXltd05kaFJNaGFNMDhwWWZGczM3My9hOXY2azlibksiLCJtYWMiOiJjOTkxNDU4OGY4MjI5YjgxM2Y2ODAzNWQzZjViYmQ2NjUzNjVmZDhhYWZiYjhlYjBlMWIyNDRjNmU1NGI0NTQwIiwidGFnIjoiIn0==",
    "ignition4_session": "eyJpdiI6Ik94UDN2TFg2UVByd3ozK0Ixd21nY0E9PSIsInZhbHVlIjoic245eWcvbW9pbWhNend5Rzg2cm9JdVJacTAwODZ1RWkyaThtZFJGNk9aRDZUd0h1N2JnYmJHN08xOVp4UEMwNThhUzh3alpocC9nWGtWejQraTdpc1dBTXA5SDlhY3VOaVcvQ3JoZDBlTERaYmpmWjJZQ2hJUmloWGFVaUpSR3EiLCJtYWMiOiI0ZTVjZTA2ZmVmMWI4MjE3ZTE4OTIyNjZlYmE3NjcwNTdjMDllMWFmNjQ0MjVmMTAzYTEzMGY3ZDEwNzVhMGY5IiwidGFnIjoiIn0==",
    "remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d": "eyJpdiI6IjVzNlM5SWxBcFd2QmkrdVFqWU1JZWc9PSIsInZhbHVlIjoibkIvWnkwVzNBVEhkY014M010VFhpZ2NmdEoxNnFneDhUa2lrbURxZENxMkNkNFNPZ0ZRREpJcXp6di96UGxXa0lQa3RreDlDU2pjSkhqSVNGMk0wUzhvbFpFa1BQa1o2RTB0N1d5WDZvbG1kS2ZuVTU2dVl2bDRlUHRZOW9IUHNiZHVXM3lIOU1sazJLelhTRFBQMnlBPT0iLCJtYWMiOiIyMDM0ZGEwMjk5NzMxN2MyNWMzODBlYTE0ZmZkNGQyNWM2MTcwMDVlNTIyNWQ4M2I2M2Y2NmNhNjIwNjUxM2I5IiwidGFnIjoiIn0=="
}

# === BUILD URL ===
params = {
    "draw": "3",
    "start": "0",
    "length": "25",
    "search[value]": SEARCH_TERM,
    "filter_preferred_platform": "windows",
    "filter_hide_abandoned": "true",
    "order[0][column]": "12",
    "order[0][dir]": "desc",
    "order[0][name]": "downloads"
}

response = requests.get("https://ignition4.customsforge.com/", headers=HEADERS, cookies=COOKIES, params=params)

print(f"🔎 Status: {response.status_code}")
try:
    data = response.json()
    results = data.get("data", [])
    print(f"✅ Found {len(results)} results:\n")
    for result in results:
        print(f"🎸 {result.get('artistName')} — {result.get('titleName')}")
        print(f"📥 Download: {result.get('file_pc_link')}")
        print("-" * 40)
except Exception as e:
    print("❌ Failed to parse JSON response")
    print(response.text)


