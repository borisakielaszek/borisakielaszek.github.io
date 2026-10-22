from pathlib import Path
import re

path = Path('jeu-vampires-de-sarrebruck/index.html')
text = path.read_text(encoding='utf-8')

# V5.66 — emblème de transition de tour.
old = '<div class="turn-notice-kicker">Les Vampires de Sarrebruck</div>'
new = '<img class="turn-notice-logo" src="assets/logo-transition-vampire.webp" alt="" aria-hidden="true">'
if old in text:
    text = text.replace(old, new, 1)
elif 'class="turn-notice-logo"' not in text:
    raise SystemExit('Turn notice kicker not found')

css = r'''
<style id="v566-turn-emblem">
.turn-notice-logo{
  display:block!important;
  width:132px!important;
  height:auto!important;
  margin:0 auto 8px!important;
  border-radius:16px!important;
  object-fit:contain!important;
  pointer-events:none!important;
}
@media(max-width:430px){
  .turn-notice-logo{width:118px!important;margin-bottom:7px!important}
}
</style>
'''
pattern = re.compile(r'<style id="v566-turn-emblem">.*?</style>', re.S)
if pattern.search(text):
    text = pattern.sub(css.strip(), text, count=1)
else:
    text = text.replace('</head>', css + '\n</head>', 1)

# V5.67 — supprime le toast de choix de cible qui restait visible par-dessus la scène de résultat.
old_attack = "if(v==='attack'){toast('Choisis maintenant la cible de ta carte.');ok=await playAttackFromHand(p,i);}"
new_attack = "if(v==='attack'){ok=await playAttackFromHand(p,i);}"
if old_attack in text:
    text = text.replace(old_attack, new_attack, 1)
elif new_attack not in text:
    raise SystemExit('Attack toast line not found')

path.write_text(text, encoding='utf-8')
