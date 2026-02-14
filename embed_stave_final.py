#!/usr/bin/env python3
import base64
from pathlib import Path

# Paths
base_dir = Path(__file__).parent
paw_patrol = base_dir / "paw_patrol"

# Read and encode images
def img_to_b64(path):
    with open(path, 'rb') as f:
        data = base64.b64encode(f.read()).decode()
    ext = path.suffix.lower()
    mime = {'jpg': 'jpeg', 'jpeg': 'jpeg', 'png': 'png', 'webp': 'webp'}
    return f"data:image/{mime.get(ext.strip('.'), 'jpeg')};base64,{data}"

print("Indlæser billeder...")

# Baggrund
bg = img_to_b64(paw_patrol / "Adventure_Bay_%28S3%29.webp")

# Cursor
cursor = img_to_b64(base_dir / "paw_cursor_mac.png")

# Avatarer
avatars = []
avatar_files = [
    'download.jpeg',
    'download (1).jpeg',
    'download (2).jpeg',
    'download (3).jpeg',
    'download (4).jpeg',
    'download (5).jpeg',
    'images.jpeg',
    'images (1).jpeg',
    'images (2).jpeg',
    'images (3).jpeg',
    'images (4).jpeg',
    'images (5).jpeg'
]

for av_file in avatar_files:
    avatars.append(img_to_b64(paw_patrol / av_file))

print("✓ Alle billeder indlæst!")

# Læs HTML
html_file = base_dir / "stave_navn.html"
with open(html_file, 'r', encoding='utf-8') as f:
    html = f.read()

# Erstat baggrund
html = html.replace("url('paw_patrol/Adventure_Bay_%28S3%29.webp')", f"url('{bg}')")

# Erstat cursor
html = html.replace("url('paw_cursor_mac.png')", f"url('{cursor}')")

# Erstat avatarer
for i, av_file in enumerate(avatar_files):
    html = html.replace(f"'paw_patrol/{av_file}'", f"'{avatars[i]}'")

# Gem
output = base_dir / "stave_navn_embedded.html"
with open(output, 'w', encoding='utf-8') as f:
    f.write(html)

size_kb = output.stat().st_size / 1024
print(f"\n✓ Genereret: {output.name}")
print(f"  Størrelse: {size_kb:.0f} KB")
print("\nÅbn stave_navn_embedded.html i din browser - alle billeder er nu embedded!")