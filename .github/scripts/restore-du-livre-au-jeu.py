from pathlib import Path
import re

path = Path('jeu-vampires-de-sarrebruck/index.html')
text = path.read_text(encoding='utf-8')

desired = "Le jeu de cartes prolonge cet univers : on y retrouve les sept vampires, les deux clans et leurs querelles. Il prend la forme d’une confrontation au cours d’une longue nuit où chacun doit survivre."
heading = '<h2>Du livre au jeu</h2>'
button = '<button id="clanStoryBackBtn"'

start = text.find(heading)
if start < 0:
    raise SystemExit('Titre « Du livre au jeu » introuvable')

button_pos = text.find(button, start)
if button_pos < 0:
    raise SystemExit('Bouton de retour de la page des origines introuvable')

between_start = start + len(heading)
between = text[between_start:button_pos]

# Retire l’éventuelle version existante de ce paragraphe pour éviter tout doublon.
paragraph_re = re.compile(r'\s*<p(?:\s+[^>]*)?>\s*Le jeu de cartes prolonge cet univers\s*:.*?</p>\s*', re.S)
cleaned = paragraph_re.sub('\n', between, count=1)

# Retire aussi l’ancien emplacement vide de l’invitation s’il subsiste.
cleaned = re.sub(r'\s*<p\s+class="story-invitation"\s*>\s*</p>\s*', '\n', cleaned, count=1, flags=re.S)

visible_paragraph = (
    '<p class="du-livre-au-jeu-text" '
    'style="display:block !important; visibility:visible !important; opacity:1 !important;">'
    f'{desired}</p>'
)

replacement = '\n      ' + visible_paragraph
if cleaned.strip():
    replacement += '\n      ' + cleaned.strip()
replacement += '\n      '

new_text = text[:between_start] + replacement + text[button_pos:]

if new_text == text:
    print('Le paragraphe est déjà visible et exactement en place.')
else:
    path.write_text(new_text, encoding='utf-8')
    print('Paragraphe « Du livre au jeu » remis en place et forcé visible.')
