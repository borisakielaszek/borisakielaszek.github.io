from pathlib import Path
import re

path = Path('jeu-vampires-de-sarrebruck/index.html')
text = path.read_text(encoding='utf-8')

# V5.69 — harmonise le panneau des actions au tutoiement.
text = text.replace('1 ACTION POSSIBLE DURANT VOTRE TOUR :', 'TES ACTIONS POSSIBLES :')

# Rend les trois actions du haut tactiles et leur associe leur section.
replacements = {
    '<li class="action-option action-option-attack">': '<li class="action-option action-option-attack" data-scroll-target="attackSection" role="button" tabindex="0" aria-label="Voir les cartes d’attaque">',
    '<li class="action-option action-option-regen">': '<li class="action-option action-option-regen" data-scroll-target="regenSection" role="button" tabindex="0" aria-label="Voir les cartes de récupération">',
    '<li class="action-option action-option-discard">': '<li class="action-option action-option-discard" data-scroll-target="discardSection" role="button" tabindex="0" aria-label="Aller à l’action défausser">',
}
for old, new in replacements.items():
    if old in text:
        text = text.replace(old, new, 1)

css = r'''
<style id="v569-action-navigation">
.drawer-help .action-option[data-scroll-target]{
  cursor:pointer!important;
  touch-action:manipulation!important;
  transition:transform .15s ease,filter .15s ease,box-shadow .15s ease!important;
}
.drawer-help .action-option[data-scroll-target]:active{transform:scale(.985)!important;filter:brightness(1.12)!important}
.drawer-help .action-option[data-scroll-target]:focus-visible{outline:2px solid #f2d38d!important;outline-offset:2px!important}
.action-card-section.action-section-pulse{animation:actionSectionPulse .7s ease!important}
@keyframes actionSectionPulse{
  0%{filter:brightness(1)}
  45%{filter:brightness(1.32);box-shadow:0 0 0 2px #f1d287aa,0 8px 28px #0008}
  100%{filter:brightness(1)}
}
</style>
'''
css_pattern = re.compile(r'<style id="v569-action-navigation">.*?</style>', re.S)
if css_pattern.search(text):
    text = css_pattern.sub(css.strip(), text, count=1)
else:
    text = text.replace('</head>', css + '\n</head>', 1)

js = r'''
<script id="v569-action-navigation-script">
(function(){
  function goToAction(option){
    if(!option)return;
    const targetId=option.getAttribute('data-scroll-target');
    const target=targetId&&document.getElementById(targetId);
    if(!target || target.classList.contains('hidden'))return;
    target.scrollIntoView({behavior:'smooth',block:'start'});
    target.classList.remove('action-section-pulse');
    void target.offsetWidth;
    target.classList.add('action-section-pulse');
    setTimeout(()=>target.classList.remove('action-section-pulse'),800);
  }
  document.addEventListener('click',function(e){
    const option=e.target.closest('#humanPanel .action-option[data-scroll-target]');
    if(option)goToAction(option);
  });
  document.addEventListener('keydown',function(e){
    if(e.key!=='Enter'&&e.key!==' ')return;
    const option=e.target.closest&&e.target.closest('#humanPanel .action-option[data-scroll-target]');
    if(!option)return;
    e.preventDefault();
    goToAction(option);
  });
})();
</script>
'''
js_pattern = re.compile(r'<script id="v569-action-navigation-script">.*?</script>', re.S)
if js_pattern.search(text):
    text = js_pattern.sub(js.strip(), text, count=1)
else:
    text = text.replace('</body>', js + '\n</body>', 1)

path.write_text(text, encoding='utf-8')

# Audit informatif : repère les restes de vouvoiement dans le code/textes.
pattern = re.compile(r'\b(vous|votre|vos|veuillez|choisissez|touchez|cliquez|pouvez|devez|voulez|êtes|avez)\b', re.I)
print('--- AUDIT VOUVOIEMENT RESTANT ---')
for no, line in enumerate(text.splitlines(), 1):
    if pattern.search(line):
        snippet = re.sub(r'\s+', ' ', line.strip())
        print(f'{no}: {snippet[:300]}')
print('--- FIN AUDIT ---')
