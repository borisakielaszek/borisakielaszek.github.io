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

# Ne toucher qu'au paragraphe de transition situé entre le titre et le bouton.
paragraph_re = re.compile(r'\s*<p(?:\s+[^>]*)?>\s*Le jeu de cartes prolonge cet univers\s*:.*?</p>\s*', re.S)
cleaned, count = paragraph_re.subn('\n', between, count=1)

# Nettoie aussi l'ancien emplacement vide éventuel, sans modifier le reste de la page.
cleaned = re.sub(r'\s*<p\s+class="story-invitation"\s*>\s*</p>\s*', '\n', cleaned, count=1, flags=re.S)

replacement = f'\n      <p>{desired}</p>\n      ' + cleaned.strip()
if cleaned.strip():
    replacement += '\n      '

new_text = text[:between_start] + replacement + text[button_pos:]

if new_text == text:
    print('Le paragraphe est déjà exactement en place.')
else:
    path.write_text(new_text, encoding='utf-8')
    print('Paragraphe « Du livre au jeu » restauré.')
