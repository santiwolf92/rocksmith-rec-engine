# cookie_helper.py
# Paste your raw cookie string when prompted, and it will create a valid cookies.py file

output_path = "cookies.py"  # Change this path if needed

raw_cookie = input("🍪 Paste your cookie string:\n")

cookie_pairs = [pair.strip() for pair in raw_cookie.split(";") if "=" in pair]
cookie_dict = {}
for pair in cookie_pairs:
    key, value = pair.split("=", 1)
    cookie_dict[key.strip()] = value.strip()

with open(output_path, "w", encoding="utf-8") as f:
    f.write("# Auto-generated cookie file\n")
    f.write(f"cookies = {cookie_dict}\n")

print(f"✅ Cookies saved to {output_path}")
