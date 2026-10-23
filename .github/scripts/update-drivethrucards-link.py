from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')

affiliate = 'https://www.drivethrucards.com/en/product/584535/The-Vampires-of-Saarbrucken?affiliate_id=5285538'

old_cover = '<figure class="game-cover"><a href="/jeu-vampires-de-sarrebruck/" aria-label="Jouer aux Vampires de Sarrebruck"><img src="/assets/jeu/couverture.webp" alt="Couverture du jeu The Vampires of Saarbrücken — édition américaine" loading="lazy" decoding="async"></a><figcaption>Édition américaine</figcaption></figure>'
new_cover = f'<figure class="game-cover"><a href="{affiliate}" target="_blank" rel="noopener noreferrer" aria-label="Acheter l’édition américaine de The Vampires of Saarbrücken sur DriveThruCards"><img src="/assets/jeu/couverture.webp" alt="Couverture du jeu The Vampires of Saarbrücken — édition américaine" loading="lazy" decoding="async"></a><figcaption>Édition américaine</figcaption></figure>'

old_availability = '<p>Le jeu sera prochainement disponible en anglais sur <strong>DriveThruCards</strong>. Les versions française et allemande sont prévues courant 2027.</p>'
new_availability = f'<p>L’édition américaine en anglais est désormais disponible à l’achat sur <strong>DriveThruCards</strong>. Les versions française et allemande sont prévues courant 2027.</p><div class="links"><a href="{affiliate}" target="_blank" rel="noopener noreferrer">Acheter la version américaine</a><a href="/jeu-vampires-de-sarrebruck/">Jouer gratuitement en ligne</a></div>'

if old_cover not in text:
    raise SystemExit('Cover link block not found; refusing unsafe patch')
if old_availability not in text:
    raise SystemExit('Availability paragraph not found; refusing unsafe patch')

text = text.replace(old_cover, new_cover, 1)
text = text.replace(old_availability, new_availability, 1)
path.write_text(text, encoding='utf-8')
