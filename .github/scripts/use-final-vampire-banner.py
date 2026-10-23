from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')

old = '''<div class="online-game-cta"><h4>Jouez aux <em>Vampires de Sarrebruck</em></h4><p>Retrouvez les vampires du livre dans une version numérique gratuite, jouable directement dans votre navigateur.</p><p><strong>Choisissez votre vampire, affrontez plusieurs adversaires contrôlés par l’IA et tentez de survivre jusqu’à l’aube.</strong></p><p class="online-game-note">Aucune installation nécessaire.</p><div class="links"><a href="/jeu-vampires-de-sarrebruck/" aria-label="Jouer en ligne aux Vampires de Sarrebruck">Entrer dans la nuit</a></div></div>'''

new = '''<div class="online-game-banner-wrap"><a href="/jeu-vampires-de-sarrebruck/" aria-label="Jouer en ligne aux Vampires de Sarrebruck"><img src="/assets/vampires-sarrebruck-banner.svg?v=20261023-final" alt="Jouez aux Vampires de Sarrebruck — version numérique gratuite" loading="lazy" decoding="async"></a></div>'''

if old not in text:
    raise SystemExit('Old online-game CTA block not found; refusing unsafe replacement')

text = text.replace(old, new, 1)

css_anchor = '.online-game-cta .links a:hover{background:#922727;border-color:#c24c4c}\n'
css_new = css_anchor + '''.online-game-banner-wrap{margin-top:3rem;width:100%;border-radius:18px;overflow:hidden;box-shadow:0 18px 42px rgba(0,0,0,.32);line-height:0}\n.online-game-banner-wrap a{display:block;width:100%}\n.online-game-banner-wrap img{display:block;width:100%;height:auto;max-width:100%;object-fit:contain}\n@media(max-width:700px){.online-game-banner-wrap{border-radius:12px;margin-top:2rem}.online-game-banner-wrap img{width:100%;height:auto;object-fit:contain}}\n'''
if '.online-game-banner-wrap{' not in text:
    if css_anchor not in text:
        raise SystemExit('CSS anchor not found; refusing unsafe CSS insertion')
    text = text.replace(css_anchor, css_new, 1)

path.write_text(text, encoding='utf-8')
