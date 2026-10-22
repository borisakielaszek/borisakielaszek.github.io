from pathlib import Path

path = Path('jeu-vampires-de-sarrebruck/index.html')
text = path.read_text(encoding='utf-8')

old = ''' const info=christmasDraw
   ? (immediate?"Cette carte à effet immédiat vient de la pioche commune pendant le Marché de Noël. Son propre effet se résout maintenant, puis la pioche du Marché de Noël reprend.":"Cette carte vient de la pioche commune. Après tes deux pioches du Marché de Noël, tu défausseras le surplus si ta main dépasse sa limite.")
   : immediate
   ? "Effet immédiat : applique l’action de cette carte maintenant."
   : (witchesBonus?"Cette carte profite immédiatement de ta nouvelle main maximale de 7.":"Prends le temps de regarder la carte avant de continuer.");'''
new = ''' const info=immediate
   ? "Effet immédiat : applique l’action de cette carte maintenant."
   : christmasDraw
   ? "Cette carte vient de la pioche commune. Après tes deux pioches du Marché de Noël, tu défausseras le surplus si ta main dépasse sa limite."
   : (witchesBonus?"Cette carte profite immédiatement de ta nouvelle main maximale de 7.":"Prends le temps de regarder la carte avant de continuer.");'''
if old not in text:
    raise SystemExit('showDrawScene info block not found')
text = text.replace(old, new, 1)

old_notice = ''' const content=`<div class="immediate-repick-notice"><div class="immediate-repick-icon">✦</div><div><strong>Effet immédiat effectué</strong><span>Tu repioches.</span></div><div class="tap-dismiss-note">Touche pour continuer</div></div>`;'''
new_notice = ''' const content=`<div class="immediate-repick-notice"><div class="immediate-repick-icon">✦</div><div><strong>Effet immédiat effectué — tu repioches.</strong></div><div class="tap-dismiss-note">Touche pour continuer</div></div>`;'''
if old_notice not in text:
    raise SystemExit('repick notice block not found')
text = text.replace(old_notice, new_notice, 1)

path.write_text(text, encoding='utf-8')
print('Immediate-effect copy harmonized.')
