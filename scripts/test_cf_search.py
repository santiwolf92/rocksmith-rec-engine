import requests

query = "stairway to heaven"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://ignition4.customsforge.com/",
    "X-Requested-With": "XMLHttpRequest",  # mimic JS frontend
}

cookies = {
    "ignition4_session": "eyJpdiI6IklmTXgrOHoyQ1RuNVdkM3U5STJMbmc9PSIsInZhbHVlIjoiVnBqOEJYUXNpRWlIbHpFMG5oeE9NMjBDc3Y1M0FGZFpxV05xMmpuWGhOcXFvS2lzRFM0Y0pvLzR1WW8zaUovRHM4R0hwWXltZVQyOU93U3c4RE5KMFRnN1JaNjY0N05pMUY4UmhzU1VxYzVzNFFHWFR2WGN4a2F2V0I3TkdUb1MiLCJtYWMiOiI4YWI2NTI0NmU1ZDExOGFhODlhN2M2NzI0ZWIwMWIzOTcyN2YxM2FiNTlhN2VjYTcxNTlhOGEwMzhhNDBjNGM0IiwidGFnIjoiIn0%3D",
    "XSRF-TOKEN": "eyJpdiI6IjMyRTZkTkVwUFhRRzBwOVArNW95Qnc9PSIsInZhbHVlIjoieW1nWlRJbG9iSDBXYldoaW8wY3hnVzJuSlNtcTRqc01OLzdZNGNMQ2hzd2FDbDhhYi9sWUVTRjFsdFhObEdIMjhzbWNnYnVjbWRmWXY1TTJ4Nm94dkRrRU5JVGtCcjlYSDlPQzhML0FqUEZBdjkyMHVVc0Z4NjBEc0haQlNHaHEiLCJtYWMiOiI0NzNjODIzMzYzYTgwY2QyYzJhYjA3NDNlNDUzMWJkYjgzM2JkMTQzYzdkYmIxMTljOGMyNzc1Yzc2NzQ3ZGM0IiwidGFnIjoiIn0%3D",
}

params = {
    "draw": 1,
    "columns[0][data]": "artistName",
    "columns[0][searchable]": "true",
    "search[value]": query,
    "length": 25,
    "start": 0,
}

url = "https://ignition4.customsforge.com/table"

response = requests.get(url, headers=headers, cookies=cookies, params=params)

print(f"🔎 Response status: {response.status_code}")
if "application/json" in response.headers.get("Content-Type", ""):
    data = response.json()
    print(f"✅ Found {len(data.get('data', []))} results:")
    for row in data.get("data", []):
        print(f"🎸 {row['artistName']} — {row['titleName']}")
else:
    print("❌ Not a JSON response:")
    print(response.text[:500])  # print first part for debugging

