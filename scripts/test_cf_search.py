import requests
import json

url = "https://ignition4.customsforge.com/tablesettings"

payload = {
    "columns[0][data]": "Title",
    "columns[1][data]": "Artist",
    "columns[2][data]": "Album",
    "columns[3][data]": "Tuning",
    "columns[4][data]": "Platform",
    "columns[5][data]": "SubmittedBy",
    "columns[6][data]": "Submitted",
    "columns[7][data]": "Rating",
    "columns[8][data]": "Version",
    "columns[9][data]": "Hits",
    "search[value]": "Stairway to Heaven",
    "start": 0,
    "length": 5,
    "draw": 3,
}

headers = {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
    "Cookie": "ips4_device_key=645bd0b959cd970cd1075abf409b8d00; ips4_forum_view=table; __eoi=ID=0348d2efe62a6935:T=1738090324:RT=1738174489:S=AA-AfjZsCqcPCcQ0w3woMKhlIiYa; ips4_cookie_consent=1; ips4_cookie_consent_optional=1; ips4_member_id=512899; ips4_login_key=ec8240b88746352dd69ed968049f03de; ips4_IPSSessionFront=d63e881b49b4a25c2749f81f7e654373; ips4_loggedIn=1753304006; XSRF-TOKEN=eyJpdiI6IkdUZmRPT2pCaWxmYVNxZVBIN0Z6Snc9PSIsInZhbHVlIjoiWnN2U0E3VU9SNVlnRDd5eDFPV2RhV215ck14NkswbEJUSDhJb0p5UmwrdGprdGgwTXNGREM1emFPK2FoQUhxRE52V2FtWm5LM0Nybmpuc3I1cllJQ0JqYkY5TmdIZHJ4SVk1eVRFNjlLRkYwbW1wdHZHczd0RldvbkZ6NzJSa3oiLCJtYWMiOiJjNjUwM2NjNWViZTlmNDg0NDI3MDYzMzA4ZWI5NmI2MWMzZmZlOTY4NWI5MTM5MGFhYzIxZjkwYzIyNDEzY2QwIiwidGFnIjoiIn0%3D; ignition4_session=eyJpdiI6IlZIVGlMK0o2ekdlV1NZWDNNNnY4ZEE9PSIsInZhbHVlIjoiaU5DK2hYYURLYlNTbTFQRzRUWXZzZWg0OWRhZlFMaEhNRkovZEZ4cm1XME5icW5LZGt5MU1ZdG1hRUJhbHlsYS9IdHdzZlJ4YVU2cEQwYm5PWFc1NmY5UGVha0VOMFQ2V0tpajAybUZmNFdFc1M4OGxVNngvTVlzOEcwcTdHTVMiLCJtYWMiOiIzYThlMzAxMWZjNjA3YjIwNzM0NTg2MmRjYjIzN2U3NDM5NmMwNzcxNjRjMTExNjdmNTJjODc0YmJlNTA1NWNiIiwidGFnIjoiIn0%3D; remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d=eyJpdiI6InJkbmdEL210ZGZHek9kUXM2UndBZHc9PSIsInZhbHVlIjoieTV0WHpJeFFpRGx5Q2RzdE1zUEZFY3hwRjVtT0g0eWk4WmQ5MDBJaDMvWkRsa2MwWlIzVW9HQTRZR1k4VVpqRzk3RDZhZXFySnExTnFRdFFxSjJqM3p1VHZCUDM4SEZEZm0ydVdpdDh5ZlcyM2NvcDU5V1RoRXgyRG54QmlyTUY0SkhnYUdWTzFpRi92OUhTb005TVVRPT0iLCJtYWMiOiJkYTQxYjE3YWFmNWRjNzllYzNmODQ3YzkwNDhkYjkyZjhiYjVkMzM4NGZjN2NjNzY2ODgxOTJlN2IzNzBkZTkzIiwidGFnIjoiIn0%3D"
}

response = requests.post(url, data=payload, headers=headers)

if response.status_code == 200:
    print("✅ Success!")
    results = response.json().get("data", [])
    for i, result in enumerate(results, 1):
        artist = result.get("artist", "Unknown Artist")
        title = result.get("title", "Unknown Title")
        downloads = result.get("downloads", 0)
        print(f"{i}. {artist} — {title} ({downloads} downloads)")
else:
    print(f"❌ Status Code: {response.status_code}")
    print(response.text)
