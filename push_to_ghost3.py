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

pages = [
    ("index", "Home", "index.html"),
    ("about", "About", "about.html"),
    ("services", "Services", "services.html"),
    ("case-studies", "Case Studies", "case-studies.html"),
    ("contact", "Contact", "contact.html"),
]

for slug, title, filename in pages:
    print(f"\n=== {title} ===")
    html = read_file(filename)
    body = re.search(r'<body>(.*?)</body>', html, re.DOTALL)
    body_content = body.group(1) if body else html
    body_content = re.sub(r'<style.*?</style>', '', body_content, flags=re.DOTALL)
    
    # Get current page to fetch updated_at
    r = requests.get(f"{BASE_URL}/ghost/api/admin/pages/slug/{slug}/", headers=headers)
    if r.status_code != 200 or not r.json().get('pages'):
        print(f"  Page not found, creating new")
        page_data = {"pages": [{"title": title, "slug": slug, "html": body_content, "status": "published"}]}
        r = requests.post(f"{BASE_URL}/ghost/api/admin/pages/", headers=headers, json=page_data)
    else:
        page = r.json()["pages"][0]
        updated_at = page["updated_at"]
        page_id = page["id"]
        
        # Update with updated_at
        page_data = {
            "pages": [{
                "title": title,
                "html": body_content,
                "status": "published",
                "updated_at": updated_at
            }]
        }
        r = requests.put(f"{BASE_URL}/ghost/api/admin/pages/{page_id}/", headers=headers, json=page_data)
    
    if r.status_code in [200, 201]:
        print(f"  ✓ Success!")
    else:
        print(f"  ✗ {r.status_code}: {r.text[:200]}")

print("\n=== DONE ===")
