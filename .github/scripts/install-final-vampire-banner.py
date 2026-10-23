from pathlib import Path
import base64

parts_dir = Path('.github/banner-parts')
parts = [parts_dir / f'part{i:02d}.txt' for i in range(9)]
missing = [str(p) for p in parts if not p.exists()]
if missing:
    raise SystemExit(f'Missing banner parts: {missing}')

data = ''.join(p.read_text(encoding='utf-8').strip() for p in parts)
if len(data) != 69808:
    raise SystemExit(f'Unexpected base64 length: {len(data)}')

raw = base64.b64decode(data, validate=True)
if len(raw) != 52354:
    raise SystemExit(f'Unexpected WebP size: {len(raw)}')
if not (raw[:4] == b'RIFF' and raw[8:12] == b'WEBP'):
    raise SystemExit('Decoded file is not a valid WebP container')

out = Path('assets/vampires-sarrebruck-banner-final.webp')
out.write_bytes(raw)

index = Path('index.html')
html = index.read_text(encoding='utf-8')
old = '/assets/vampires-sarrebruck-banner.svg?v=20261023-final'
new = '/assets/vampires-sarrebruck-banner-final.webp?v=20261023-mobilefix2'
if old not in html:
    if new not in html:
        raise SystemExit('Banner reference not found in index.html')
else:
    html = html.replace(old, new, 1)
    index.write_text(html, encoding='utf-8')

print(f'Installed {out} ({len(raw)} bytes) and updated index.html')
