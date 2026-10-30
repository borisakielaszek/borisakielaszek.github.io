from pathlib import Path
import re

src = Path('jeu-vampires-de-sarrebruck/index.html')
out = Path('tmp-vampire-tutorial-context.txt')
text = src.read_text(encoding='utf-8')

terms = [
    'Entrer dans la nuit', 'ENTRER DANS LA NUIT', 'Entrer', 'première fois',
    '⚡', '🛡', '🩸', 'bouclier', 'Bouclier', 'goutte', 'Goutte',
    'sablier', 'Sablier', 'hourglass', 'shield', 'lightning',
    'passer son tour', 'Passe son tour', 'défense impossible',
    'humanCardClick', 'drawer-help', 'CARDS=', 'const CARDS',
]

parts = []
for term in terms:
    starts = [m.start() for m in re.finditer(re.escape(term), text, flags=re.I if term.isascii() else 0)]
    parts.append(f'\n===== TERM: {term!r} ({len(starts)} occurrences) =====\n')
    for idx, pos in enumerate(starts[:12]):
        a = max(0, pos - 1800)
        b = min(len(text), pos + 2600)
        parts.append(f'\n--- occurrence {idx+1} @ {pos} ---\n{text[a:b]}\n')

# Also capture likely entry buttons and help/action blocks.
patterns = {
    'buttons containing nuit/entrer': r'<button[^>]*>[^<]*(?:nuit|entrer)[^<]*</button>',
    'elements containing nuit/entrer': r'<[^>]+>[^<]{0,120}(?:nuit|entrer)[^<]{0,120}</[^>]+>',
    'card icon-ish strings': r'[^\n]{0,180}(?:⚡|🛡|🩸|goutte|bouclier|sablier)[^\n]{0,240}',
}
for label, pat in patterns.items():
    parts.append(f'\n===== REGEX: {label} =====\n')
    matches = re.findall(pat, text, flags=re.I)
    for m in matches[:100]:
        parts.append(m + '\n')

out.write_text(''.join(parts), encoding='utf-8')
print(f'wrote {out} ({out.stat().st_size} bytes)')
