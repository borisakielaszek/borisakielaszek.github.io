from pathlib import Path
import base64
import re

svg_path = Path('assets/vampires-sarrebruck-banner.svg')
out_path = Path('assets/vampires-sarrebruck-banner-final.webp')
index_path = Path('index.html')

svg = svg_path.read_text(encoding='utf-8')
match = re.search(r'data:image/webp;base64,([^"\']+)', svg)
if not match:
    raise SystemExit('Embedded WebP not found in banner SVG')

raw = base64.b64decode(match.group(1))
if not (raw.startswith(b'RIFF') and raw[8:12] == b'WEBP'):
    raise SystemExit('Decoded banner is not a valid WebP')
out_path.write_bytes(raw)

html = index_path.read_text(encoding='utf-8')
old = '/assets/vampires-sarrebruck-banner.svg?v=20261023-final'
new = '/assets/vampires-sarrebruck-banner-final.webp?v=20261023-mobilefix'
if old not in html:
    raise SystemExit('Expected SVG banner reference not found in index.html')
html = html.replace(old, new, 1)
index_path.write_text(html, encoding='utf-8')

print(f'Wrote {out_path} ({len(raw)} bytes) and updated index.html')
