import jwt
import time
import requests
import re

def read_file(path):
    with open(path, 'r') as f:
        return f.read()

key = "69c01ab69d9f6f0001cf76e3:e74200bfddb31147de9c40d56b6d51f3a2f2e466750adca7cbb678159500a754"
id_, secret = key.split(":")
iat = int(time.time())
token = jwt.encode(
    {"iat": iat, "exp": iat+300, "aud": "/admin/"},
    bytes.fromhex(secret),
    algorithm="HS256",
    headers={"kid": id_}
)
headers = {"Authorization": f"Ghost {token}", "Content-Type": "application/json"}

BASE_URL = "https://zanoma.ghost.io"

# Inject code into site settings to override theme
html = read_file("index.html")

# Extract body content  
body = re.search(r'<body>(.*?)</body>', html, re.DOTALL)
body_content = body.group(1) if body else html

# Get current settings
r = requests.get(f"{BASE_URL}/ghost/api/admin/settings/", headers=headers)
settings = r.json()["settings"]

# Find codeinjection_head setting
for s in settings:
    if s["key"] == "codeinjection_head":
        head_setting = s
    if s["key"] == "codeinjection_foot":
        foot_setting = s

# We'll inject into site-wide header to override everything
inject_code = f"""
<style>
{{-ms-high-contrast-adjust: none;}} 
:root {{
  --bg: #0a0a0f;
  --bg2: #12121a;
  --green: #39FF14;
  --green-dim: rgba(57,255,20,0.15);
  --text: #f0f0f5;
  --text-muted: #8888a0;
  --border: rgba(255,255,255,0.08);
  --radius: 16px;
}}
body {{
  background: var(--bg) !important;
  color: var(--text) !important;
  font-family: 'Inter', -apple-system, sans-serif !important;
}}
.site-nav, .gh-head, header, nav, footer, .content-cover, .gh-canvas, .gh-article, .gh-main, main {{
  display: none !important;
}}
html {{ background: var(--bg) !important; }}
body {{ 
  background: var(--bg) !important;
  background-image: 
    linear-gradient(rgba(57,255,20,0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(57,255,20,0.03) 1px, transparent 1px) !important;
  background-size: 60px 60px !important;
}}
a {{ color: var(--green) !important; }}
</style>
"""

# Try to update site code injection
settings_data = {
    "settings": [
        {
            "key": "codeinjection_head",
            "value": inject_code
        }
    ]
}

r = requests.put(f"{BASE_URL}/ghost/api/admin/settings/", headers=headers, json=settings_data)
print(f"Code injection result: {r.status_code}")
if r.status_code == 200:
    print("✓ Injected CSS override")
else:
    print(f"Error: {r.text[:200]}")
