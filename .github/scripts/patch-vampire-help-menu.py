from pathlib import Path
import re

path = Path('jeu-vampires-de-sarrebruck/index.html')
text = path.read_text(encoding='utf-8')

# V5.64 — réactive une vraie transition cliquable entre deux tours.
turn_css = r'''
<style id="v564-turn-transition">
.turn-notice{display:flex!important;cursor:pointer!important;touch-action:manipulation!important}
.turn-notice-card{cursor:pointer!important;user-select:none!important;-webkit-user-select:none!important}
.turn-notice-text{margin-top:10px!important;font-weight:700!important}
.turn-notice-vamp{margin-top:12px!important;color:#d7c5a9!important;font-weight:700!important}
</style>
'''

turn_style_pattern = re.compile(r'<style id="v564-turn-transition">.*?</style>', re.S)
if turn_style_pattern.search(text):
    text = turn_style_pattern.sub(turn_css.strip(), text, count=1)
else:
    if '</head>' not in text:
        raise SystemExit('Missing </head>')
    text = text.replace('</head>', turn_css + '\n</head>', 1)

old_notice = '''async function showTurnNotice(p){
 // V5.27 : aucune seconde annonce de tour ici.
 // logTurnStart() écrit déjà l'unique ligne « Au tour de … » dans le Journal nocturne.
 return;
}'''

new_notice = '''async function showTurnNotice(p){
 const notice=el('turnNotice');
 if(!notice)return;
 const nameEl=el('turnNoticeName'),textEl=el('turnNoticeText'),vampEl=el('turnNoticeVamp');
 const vampireName=VAMPIRES[p.vampire]?.name||'';
 if(nameEl)nameEl.textContent=`Le tour de ${pName(p)}`;
 if(textEl)textEl.textContent='commence…';
 if(vampEl)vampEl.textContent=`${vampireName}${vampireName?' • ':''}Touchez pour continuer`;
 notice.setAttribute('aria-hidden','false');
 notice.setAttribute('role','button');
 notice.setAttribute('tabindex','0');
 notice.setAttribute('aria-label',`Le tour de ${pName(p)} commence. Touchez pour continuer.`);
 notice.classList.add('show');
 await new Promise(resolve=>{
   let closed=false;
   const finish=()=>{
     if(closed)return;
     closed=true;
     notice.classList.remove('show');
     notice.setAttribute('aria-hidden','true');
     notice.removeEventListener('click',finish);
     notice.removeEventListener('keydown',onKey);
     setTimeout(resolve,140);
   };
   const onKey=e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();finish();}};
   notice.addEventListener('click',finish);
   notice.addEventListener('keydown',onKey);
   try{notice.focus({preventScroll:true});}catch(e){}
 });
}'''

if old_notice in text:
    text = text.replace(old_notice, new_notice, 1)
elif 'async function showTurnNotice(p)' in text and 'Touchez pour continuer' not in text:
    raise SystemExit('showTurnNotice exists but no longer matches the expected old version')

# V5.65 — la bannière rouge de pioche devient l'en-tête visuel de la fenêtre.
draw_css = r'''
<style id="v565-endturn-draw-header">
.draw-scene .draw-kicker{
  grid-column:1/-1!important;
  grid-row:1!important;
  width:100%!important;
  margin:0 0 6px!important;
  box-sizing:border-box!important;
}
@media(max-width:640px){
  .draw-scene .draw-kicker{margin-bottom:2px!important}
}
</style>
'''
draw_style_pattern = re.compile(r'<style id="v565-endturn-draw-header">.*?</style>', re.S)
if draw_style_pattern.search(text):
    text = draw_style_pattern.sub(draw_css.strip(), text, count=1)
else:
    if '</head>' not in text:
        raise SystemExit('Missing </head>')
    text = text.replace('</head>', draw_css + '\n</head>', 1)

old_title = 'const title=christmasDraw?"Marché de Noël — pioche commune":witchesBonus?"Carte supplémentaire":(immediate?"Carte Éclair révélée !":"Carte piochée");'
new_title = 'const title=christmasDraw?"Marché de Noël — pioche commune":witchesBonus?"Carte supplémentaire":"";'
if old_title in text:
    text = text.replace(old_title, new_title, 1)
elif new_title not in text:
    raise SystemExit('draw scene title line not found')

old_content = 'const content=`<div class="immediate-scene draw-scene"><img src="${imgCard(id)}" alt="${cardName(id)}"><div class="immediate-scene-copy"><div class="scene-kicker draw-kicker">${kicker}</div><div class="scene-title">${cardName(id)}</div><div class="scene-text">${info}</div><div class="scene-small">${immediate?"Son effet se déclenchera quand tu continueras.":"La carte rejoint ta main."}</div><div class="tap-dismiss-note">Touche cette notification pour continuer</div></div></div>`;'
new_content = 'const content=`<div class="immediate-scene draw-scene"><div class="scene-kicker draw-kicker">${kicker}</div><img src="${imgCard(id)}" alt="${cardName(id)}"><div class="immediate-scene-copy"><div class="scene-title">${cardName(id)}</div><div class="scene-text">${info}</div><div class="scene-small">${immediate?"Son effet se déclenchera quand tu continueras.":"La carte rejoint ta main."}</div><div class="tap-dismiss-note">Touche cette notification pour continuer</div></div></div>`;'
if old_content in text:
    text = text.replace(old_content, new_content, 1)
elif new_content not in text:
    raise SystemExit('draw scene content block not found')

path.write_text(text, encoding='utf-8')
