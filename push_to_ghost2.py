import jwt
import time
import requests
import re
import json

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

# Helper to convert HTML to Ghost's expected format
def html_to_mobiledoc(html_content):
    # Simple conversion - Ghost expects mobiledoc format
    # For now, let's just try HTML format
    return html_content

pages = [
    ("index", "Home", "index.html"),
    ("about", "About", "about.html"),
    ("services", "Services", "services.html"),
    ("case-studies", "Case Studies", "case-studies.html"),
    ("contact", "Contact", "contact.html"),
]

for slug, title, filename in pages:
    print(f"\n=== Uploading {title} ({slug}) ===")
    html = read_file(filename)
    
    # Extract body content
    body = re.search(r'<body>(.*?)</body>', html, re.DOTALL)
    body_content = body.group(1) if body else html
    
    # Clean up the content - remove our custom styles that conflict with Ghost
    body_content = re.sub(r'<style.*?</style>', '', body_content, flags=re.DOTALL)
    body_content = re.sub(r'<script.*?</script>', '', body_content, flags=re.DOTALL)
    
    # Use HTML format (modern Ghost)
    page_data = {
        "pages": [{
            "title": title,
            "slug": slug,
            "html": body_content,
            "status": "published",
            "meta_description": f"Zanoma {title} - AI Solutions for Brands, Retailers, and Sellers"
        }]
    }
    
    # Check if page exists and get ID
    r = requests.get(f"{BASE_URL}/ghost/api/admin/pages/slug/{slug}/", headers=headers)
    
    if r.status_code == 200 and r.json().get('pages'):
        page_id = r.json()["pages"][0]["id"]
        print(f"  Updating existing page ID: {page_id}")
        r = requests.put(f"{BASE_URL}/ghost/api/admin/pages/{page_id}/", headers=headers, json=page_data)
    elif r.status_code == 404:
        print(f"  Creating new page")
        r = requests.post(f"{BASE_URL}/ghost/api/admin/pages/", headers=headers, json=page_data)
    else:
        print(f"  Unexpected status: {r.status_code}")
        continue
    
    if r.status_code in [200, 201]:
        # Now publish it
        page = r.json().get("pages", [{}])[0]
        page_id = page.get("id")
        if page.get("status") == "draft" and page_id:
            print(f"  Publishing page...")
            r = requests.put(f"{BASE_URL}/ghost/api/admin/pages/{page_id}/", 
                           headers=headers, 
                           json={"pages": [{"status": "published"}]})
        print(f"  ✓ Success!")
    else:
        print(f"  ✗ Error: {r.status_code}")
        print(f"  {r.text[:300]}")

print("\n=== Done ===")
