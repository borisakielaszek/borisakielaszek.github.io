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

path.write_text(text, encoding='utf-8')
