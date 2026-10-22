from pathlib import Path
import re

path = Path('jeu-vampires-de-sarrebruck/index.html')
text = path.read_text(encoding='utf-8')

old_can = """function canPlayAttack(p,id){
 if(id==='hypnose')return alivePlayers().some(t=>t!==p&&t.vampire!=='elisabetta'&&(t.hand.length||t.witches)) || (p.vampire==='elisabetta'&&alivePlayers().filter(t=>t!==p).length>=2);
 if(id==='lycanthrope'||id==='meute')return alivePlayers().some(t=>t!==p&&t.vampire!=='rudiger');
 if(id==='poche_perimee'&&p.vampire==='ermanno')return true;
 return alivePlayers().some(t=>t!==p);
}"""
new_can = """function attackBlockReason(attacker,id){
 const opponents=alivePlayers().filter(t=>t!==attacker&&t.alive);
 if(!opponents.length)return 'Aucun adversaire vivant ne peut être ciblé.';
 if((id==='lycanthrope'||id==='meute')&&opponents.every(t=>t.vampire==='rudiger'))return 'Rüdiger est immunisé contre les attaques de lycanthropes.';
 if(id==='hypnose'){
   if(attacker.vampire==='elisabetta'&&opponents.length>=2)return '';
   const stealable=opponents.filter(t=>t.vampire!=='elisabetta'&&(t.hand.length||t.witches));
   if(!stealable.length){
     if(opponents.every(t=>t.vampire==='elisabetta'))return 'Elisabetta est immunisée à l’Hypnose.';
     return 'Aucun adversaire ne possède de carte que l’Hypnose peut voler.';
   }
 }
 if(isHunter(id)&&opponents.every(t=>t.vampire==='ilsa'))return 'Ilsa est immunisée aux chasseurs.';
 if(id==='saint_nicolas'&&opponents.every(t=>t.vampire==='elisabetta'))return 'Elisabetta ne passe jamais son tour.';
 if(id==='poche_perimee'&&opponents.every(t=>t.vampire==='ermanno'))return 'Ermanno est immunisé contre la Poche périmée.';
 return '';
}
function attackUnavailableLabel(attacker,id){
 const reason=attackBlockReason(attacker,id);
 if(!reason)return '';
 if(reason.includes('Rüdiger'))return 'RÜDIGER IMMUNISÉ';
 if(reason.includes('Elisabetta'))return 'ELISABETTA IMMUNISÉE';
 if(reason.includes('Ilsa'))return 'ILSA IMMUNISÉE';
 if(reason.includes('Ermanno'))return 'ERMANNO IMMUNISÉ';
 return 'AUCUNE CIBLE';
}
function validAttackTargets(attacker,id){
 let targets=alivePlayers().filter(t=>t!==attacker&&t.alive);
 if(id==='hypnose')targets=targets.filter(t=>t.vampire!=='elisabetta'&&(t.hand.length||t.witches));
 if(id==='lycanthrope'||id==='meute')targets=targets.filter(t=>t.vampire!=='rudiger');
 if(isHunter(id))targets=targets.filter(t=>t.vampire!=='ilsa');
 if(id==='saint_nicolas')targets=targets.filter(t=>t.vampire!=='elisabetta');
 if(id==='poche_perimee')targets=targets.filter(t=>t.vampire!=='ermanno');
 return targets;
}
function canPlayAttack(p,id){
 if(id==='impots')return alivePlayers().some(t=>t!==p);
 if(id==='hypnose'&&p.vampire==='elisabetta'&&alivePlayers().filter(t=>t!==p).length>=2)return true;
 return validAttackTargets(p,id).length>0;
}"""
if old_can in text:
    text = text.replace(old_can, new_can, 1)
elif 'function attackBlockReason(attacker,id)' not in text:
    raise SystemExit('canPlayAttack block not found')

old_hand = "const handCardHTML=(cid,i)=>`<div class=\"hand-card ${playable?'playable':''}\" data-index=\"${i}\"><img src=\"${imgCard(cid)}\" alt=\"${cardName(cid)}\"><div class=\"cardtag\">${cardName(cid)}</div></div>`;"
new_hand = """const handCardHTML=(cid,i)=>{const kind=CARDS[cid]?.kind;const altUse=(h.vampire==='rudiger'&&(cid==='lycanthrope'||cid==='meute'))||(h.vampire==='ermanno'&&cid==='poche_perimee');const blocked=playable&&(kind==='attack'||kind==='hybrid')&&!canPlayAttack(h,cid)&&!altUse;const badge=blocked?`<div class=\"card-unavailable-badge\">${attackUnavailableLabel(h,cid)}</div>`:'';return `<div class=\"hand-card ${playable?'playable':''} ${blocked?'attack-unavailable':''}\" data-index=\"${i}\"><div class=\"hand-card-image-wrap\"><img src=\"${imgCard(cid)}\" alt=\"${cardName(cid)}\">${badge}</div><div class=\"cardtag\">${cardName(cid)}</div></div>`;};"""
if old_hand in text:
    text = text.replace(old_hand, new_hand, 1)
elif 'card-unavailable-badge' not in text:
    raise SystemExit('handCardHTML block not found')

old_copy = "if(c.kind==='attack'||c.kind==='hybrid') return `<div class=\"action-copy attack\"><div class=\"action-kicker\">⚔ ATTAQUE</div><div class=\"action-main\">${attackPreviewText(p,id)}</div><div class=\"action-question\">Veux-tu lancer cette attaque ?</div></div>`;"
new_copy = """if(c.kind==='attack'||c.kind==='hybrid'){
   const reason=attackBlockReason(p,id);
   if(!canPlayAttack(p,id)&&reason)return `<div class=\"action-copy attack unavailable-action\"><div class=\"action-kicker\">⚔ ATTAQUE</div><div class=\"action-main\">${attackPreviewText(p,id)}</div><div class=\"attack-immunity-note\"><strong>Impossible pour l’instant :</strong> ${reason}</div></div>`;
   return `<div class=\"action-copy attack\"><div class=\"action-kicker\">⚔ ATTAQUE</div><div class=\"action-main\">${attackPreviewText(p,id)}</div><div class=\"action-question\">Veux-tu lancer cette attaque ?</div></div>`;
 }"""
if old_copy in text:
    text = text.replace(old_copy, new_copy, 1)
elif 'attack-immunity-note' not in text:
    raise SystemExit('cardActionCopy attack branch not found')

old_buttons = """if(c.kind==='attack')buttons.push({label:'⚔ Lancer l’attaque',value:'attack',className:'danger'});
   if(c.kind==='regen')buttons.push({label:'🩸 Utiliser maintenant',value:'regen',className:'good'});
   if(c.kind==='hybrid')buttons.push({label:'⚔ Lancer l’attaque',value:'attack',className:'danger'});"""
new_buttons = """if(c.kind==='attack'&&canPlayAttack(p,id))buttons.push({label:'⚔ Lancer l’attaque',value:'attack',className:'danger'});
   if(c.kind==='regen')buttons.push({label:'🩸 Utiliser maintenant',value:'regen',className:'good'});
   if(c.kind==='hybrid'&&canPlayAttack(p,id))buttons.push({label:'⚔ Lancer l’attaque',value:'attack',className:'danger'});"""
if old_buttons in text:
    text = text.replace(old_buttons, new_buttons, 1)
elif "c.kind==='attack'&&canPlayAttack(p,id)" not in text:
    raise SystemExit('humanCardClick buttons block not found')

old_play = "async function playAttackFromHand(p,i){const id=p.hand[i];if(!canPlayAttack(p,id)){toast('Aucune cible valable pour cette attaque.');return false}"
new_play = "async function playAttackFromHand(p,i){const id=p.hand[i];if(!canPlayAttack(p,id)){toast(attackBlockReason(p,id)||'Aucune cible valable pour cette attaque.');return false}"
if old_play in text:
    text = text.replace(old_play, new_play, 1)
elif "toast(attackBlockReason(p,id)" not in text:
    raise SystemExit('playAttackFromHand guard not found')

old_candidates = """let candidates=alivePlayers().filter(t=>t!==attacker);
 if(id==='hypnose')candidates=candidates.filter(t=>t.vampire!=='elisabetta'&&(t.hand.length||t.witches));
 if(id==='lycanthrope'||id==='meute')candidates=candidates.filter(t=>t.vampire!=='rudiger');
 if(id==='poche_perimee'&&attacker.vampire==='ermanno')candidates.push(attacker);
 let target=forcedTarget||(attacker.human?await choosePlayer(`Cible de ${cardName(id)}`,candidates,true):aiTarget(attacker,candidates,id));if(!target){toast('Aucune cible choisie.');return false;}"""
new_candidates = """let candidates=validAttackTargets(attacker,id);
 let target=forcedTarget||(attacker.human?await choosePlayer(`Cible de ${cardName(id)}`,candidates,true):aiTarget(attacker,candidates,id));if(!target){toast(attackBlockReason(attacker,id)||'Aucune cible choisie.');return false;}"""
if old_candidates in text:
    text = text.replace(old_candidates, new_candidates, 1)
elif 'let candidates=validAttackTargets(attacker,id);' not in text:
    raise SystemExit('executeAttack candidate block not found')

css = r'''
<style id="v570-immunity-targets">
.hand-card-image-wrap{position:relative!important}
.hand-card.attack-unavailable .hand-card-image-wrap img{filter:grayscale(.72) brightness(.48)!important;opacity:.72!important}
.card-unavailable-badge{
  position:absolute!important;
  left:6px!important;right:6px!important;bottom:8px!important;
  z-index:3!important;
  padding:6px 5px!important;
  border:1px solid #e5b66a!important;
  border-radius:9px!important;
  background:#160b0de8!important;
  color:#f6dca7!important;
  text-align:center!important;
  font-family:system-ui,sans-serif!important;
  font-size:.68rem!important;
  font-weight:900!important;
  line-height:1.1!important;
  letter-spacing:.04em!important;
  box-shadow:0 4px 12px #000a!important;
}
.attack-immunity-note{
  margin-top:14px!important;
  padding:12px 13px!important;
  border:1px solid #b04b58!important;
  border-radius:12px!important;
  background:#351016!important;
  color:#ffe3d6!important;
  line-height:1.35!important;
}
</style>
'''
pat = re.compile(r'<style id="v570-immunity-targets">.*?</style>', re.S)
if pat.search(text):
    text = pat.sub(css.strip(), text, count=1)
else:
    text = text.replace('</head>', css + '\n</head>', 1)

path.write_text(text, encoding='utf-8')
print('V5.70 immunity-aware targeting applied')
