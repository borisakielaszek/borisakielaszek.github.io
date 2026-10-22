from pathlib import Path
import re

path = Path('jeu-vampires-de-sarrebruck/index.html')
text = path.read_text(encoding='utf-8')

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

path.write_text(text, encoding='utf-8')
