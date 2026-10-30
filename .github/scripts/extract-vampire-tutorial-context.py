from pathlib import Path
import re

src = Path('jeu-vampires-de-sarrebruck/index.html')
out = Path('tmp-vampire-tutorial-context.txt')
text = src.read_text(encoding='utf-8')

parts = []

def around(label, term, pre=1400, post=4200, limit=12, flags=0):
    starts = [m.start() for m in re.finditer(re.escape(term), text, flags=flags)]
    parts.append(f'\n===== {label}: {term!r} ({len(starts)} occurrences) =====\n')
    for idx, pos in enumerate(starts[:limit]):
        a = max(0, pos-pre); b = min(len(text), pos+post)
        parts.append(f'\n--- occurrence {idx+1} @ {pos} ---\n{text[a:b]}\n')

around('ENTRY BUTTON', 'enterNightBtn', 1800, 5000, 10)
around('QUICK GUIDE', 'quickGuideBtn', 1800, 6500, 10)
around('GUIDE TEXT', 'Comprendre le jeu en une minute', 1800, 9000, 5)
around('ICON LIGHTNING FR', 'éclair', 1600, 4000, 12, re.I)
around('ICON SHIELD FR', 'bouclier', 1600, 4000, 12, re.I)
around('ICON DROP FR', 'goutte', 1400, 3200, 20, re.I)
around('ICON HOURGLASS FR', 'sablier', 1400, 3200, 12, re.I)
around('ICON HOURGLASS', 'hourglass', 1400, 3200, 12, re.I)
around('ICON BADGE', 'action-icon-badge', 1400, 4500, 12)
around('CARDS DEF', 'const CARDS', 500, 34000, 2)
around('CARD EXPLAIN', 'CARD_EXPLAIN', 1000, 15000, 4)

# Extract the compact HTML section containing the current quick guide if present.
for marker in ['id="quickGuide', 'id="guide', 'quick-guide', 'guide-screen']:
    pos = text.find(marker)
    if pos >= 0:
        parts.append(f'\n===== GUIDE MARKER {marker!r} @ {pos} =====\n')
        parts.append(text[max(0,pos-1200):min(len(text),pos+18000)])

out.write_text(''.join(parts), encoding='utf-8')
print(f'wrote {out} ({out.stat().st_size} bytes)')
