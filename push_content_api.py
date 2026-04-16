import jwt
import time
import requests
import re
import json

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

# Use content API key
CONTENT_KEY = "aaa9427a44d7a2f4cf4b305c4b"

def read_file(path):
    with open(path, 'r') as f:
        return f.read()

# Let's just delete all pages and recreate via content API
# Actually, let's try posting to the content API instead

# First, let's see what pages exist
r = requests.get(f"{BASE_URL}/ghost/api/admin/pages/?limit=all", headers=headers)
pages = r.json().get("pages", [])
print(f"Found {len(pages)} pages")
for p in pages:
    print(f"  - {p['slug']}: {p['title']} (html len: {len(p.get('html',''))})")
