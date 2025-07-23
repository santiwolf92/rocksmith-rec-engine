import requests

headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Referer": "https://ignition4.customsforge.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0",
    "X-Requested-With": "XMLHttpRequest"
}

cookies = {
    # Insert the **minimal** necessary cookies here
    # Usually: ips4_member_id, ips4_login_key, XSRF-TOKEN, ignition4_session
}

params = {
    "draw": 3,
    "start": 0,
    "length": 25,
    "search[value]": "Stairway to heaven",
    "filter_preferred_platform": "windows",
    "filter_hide_abandoned": "true",
    "_": "1753304693702"
}

url = "https://ignition4.customsforge.com/"

response = requests.get(url, headers=headers, cookies=cookies, params=params)
print(f"🔎 Status: {response.status_code}")
try:
    data = response.json()
    print(f"✅ Found {len(data.get('data', []))} results:")
    for r in data.get("data", []):
        print(f"- {r.get('artistName')} — {r.get('titleName')}")
except Exception as e:
    print("⚠️ Could not parse response as JSON")
    print(response.text)



