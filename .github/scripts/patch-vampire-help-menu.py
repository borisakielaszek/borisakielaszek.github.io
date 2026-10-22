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

# V5.68 — nouvelle présentation de la main : 3 actions colorées + cartes regroupées par action.
new_drawer = '''<div class="drawer-help">
        <div class="drawer-help-title">1 ACTION POSSIBLE DURANT VOTRE TOUR :</div>
        <ul>
          <li class="action-option action-option-attack"><span class="action-number">1.</span><span class="action-key">ATTAQUER</span></li>
          <li class="action-option action-option-regen"><span class="action-number">2.</span><span class="action-key">RÉCUPÉRER</span></li>
          <li class="action-option action-option-discard"><span class="action-number">3.</span><span class="action-key">DÉFAUSSER</span><span class="action-detail">défausser 1 carte pour en piocher une nouvelle.</span></li>
        </ul>
      </div>
      <div class="drawer-choice-title">Choisis ton action :</div>
      <div id="humanHand" class="action-card-groups">
        <section id="attackSection" class="action-card-section attack-section">
          <div class="action-section-title">⚔ Cartes d’attaque</div>
          <div id="attackHand" class="hand drawer-group-hand"></div>
        </section>
        <section id="regenSection" class="action-card-section regen-section">
          <div class="action-section-title">🩸 Cartes de récupération</div>
          <div id="regenHand" class="hand drawer-group-hand"></div>
          <div class="human-actions drawer-actions drawer-regen-actions">
            <button id="manfredBtn" class="secondary hidden">Pouvoir de Manfred +1 🩸</button>
          </div>
        </section>
        <section id="discardSection" class="action-card-section discard-section">
          <div class="action-section-title">↻ Défausser et piocher une nouvelle carte</div>
          <div class="human-actions drawer-actions">
            <button id="exchangeBtn" class="secondary">Choisir une carte à défausser</button>
          </div>
        </section>
        <section id="defenseSection" class="action-card-section defense-section hidden">
          <div class="action-section-title">🛡 Cartes de défense</div>
          <div id="defenseHand" class="hand drawer-group-hand"></div>
        </section>
        <section id="otherSection" class="action-card-section other-section hidden">
          <div class="action-section-title">Autres cartes</div>
          <div id="otherHand" class="hand drawer-group-hand"></div>
        </section>
      </div>'''

drawer_pattern = re.compile(
    r'<div class="drawer-help">.*?<div id="humanHand" class="hand"></div>',
    re.S,
)
if drawer_pattern.search(text):
    text = drawer_pattern.sub(new_drawer, text, count=1)
elif 'id="attackHand"' not in text:
    raise SystemExit('Drawer block not found')

old_render = "el('humanHand').innerHTML=h.hand.map((cid,i)=>`<div class=\"hand-card ${playable?'playable':''}\" data-index=\"${i}\"><img src=\"${imgCard(cid)}\" alt=\"${cardName(cid)}\"><div class=\"cardtag\">${cardName(cid)}</div></div>`).join('');\n   [...el('humanHand').querySelectorAll('.hand-card')].forEach(n=>n.addEventListener('click',()=>humanCardClick(Number(n.dataset.index))));"
new_render = """const handCardHTML=(cid,i)=>`<div class=\"hand-card ${playable?'playable':''}\" data-index=\"${i}\"><img src=\"${imgCard(cid)}\" alt=\"${cardName(cid)}\"><div class=\"cardtag\">${cardName(cid)}</div></div>`;
   const attackCards=[],regenCards=[],defenseCards=[],otherCards=[];
   h.hand.forEach((cid,i)=>{const kind=CARDS[cid]?.kind;if(kind==='attack'||kind==='hybrid')attackCards.push([cid,i]);else if(kind==='regen')regenCards.push([cid,i]);else if(kind==='defense')defenseCards.push([cid,i]);else otherCards.push([cid,i]);});
   const fillHand=(handId,sectionId,cards,force=false)=>{const hand=el(handId),section=el(sectionId);if(hand)hand.innerHTML=cards.map(([cid,i])=>handCardHTML(cid,i)).join('');if(section)section.classList.toggle('hidden',!force&&!cards.length);};
   fillHand('attackHand','attackSection',attackCards);
   fillHand('regenHand','regenSection',regenCards,h.vampire==='manfred');
   fillHand('defenseHand','defenseSection',defenseCards);
   fillHand('otherHand','otherSection',otherCards);
   [...document.querySelectorAll('#humanPanel .hand-card')].forEach(n=>n.addEventListener('click',()=>humanCardClick(Number(n.dataset.index))));"""
if old_render in text:
    text = text.replace(old_render, new_render, 1)
elif "fillHand('attackHand','attackSection'" not in text:
    raise SystemExit('Human hand render block not found')

css568 = r'''
<style id="v568-action-drawer">
/* En-tête des 3 actions */
.drawer-help{
  margin:10px 0 12px!important;
  padding:12px!important;
  border:1px solid #5b2b31!important;
  border-radius:18px!important;
  background:linear-gradient(180deg,#171118,#0c0d13)!important;
  box-shadow:0 8px 24px #0006,inset 0 1px 0 #ffffff0b!important;
}
.drawer-help-title{
  display:block!important;
  margin:0 0 10px!important;
  padding:4px 8px 9px!important;
  text-align:center!important;
  border:0!important;
  border-radius:0!important;
  background:transparent!important;
  color:#f4dfb8!important;
  font-family:Georgia,"Times New Roman",serif!important;
  font-size:1.05rem!important;
  font-weight:800!important;
  letter-spacing:.02em!important;
}
.drawer-help ul{display:grid!important;gap:8px!important;margin:0!important;padding:0!important;list-style:none!important}
.drawer-help .action-option{
  display:grid!important;
  grid-template-columns:auto 1fr!important;
  align-items:center!important;
  column-gap:7px!important;
  min-height:58px!important;
  padding:11px 14px!important;
  border-radius:14px!important;
  box-shadow:inset 0 1px 0 #ffffff12!important;
}
.drawer-help .action-number{font-size:1.13rem!important;font-weight:900!important;color:#fff0d5!important}
.drawer-help .action-key{display:inline!important;margin:0!important;font-size:1.12rem!important;color:#fff4df!important;letter-spacing:.025em!important}
.drawer-help .action-detail{grid-column:1/-1!important;margin-top:3px!important;font-size:.92rem!important;line-height:1.3!important;color:#eee6dc!important}
.drawer-help .action-option-attack{border:1px solid #b72c38!important;background:linear-gradient(135deg,#77131c,#3d0d13)!important}
.drawer-help .action-option-regen{border:1px solid #278b54!important;background:linear-gradient(135deg,#0f5c35,#0a2f20)!important}
.drawer-help .action-option-discard{border:1px solid #7052b8!important;background:linear-gradient(135deg,#402578,#211843)!important}
.drawer-subhint{display:none!important}
.drawer-choice-title{
  margin:12px 0 9px!important;
  text-align:center!important;
  color:#f3dfba!important;
  font-family:Georgia,"Times New Roman",serif!important;
  font-size:1.35rem!important;
  font-weight:900!important;
}
.action-card-groups{display:grid!important;gap:12px!important;width:100%!important}
.action-card-section{
  overflow:hidden!important;
  border-radius:17px!important;
  border:1px solid #3b4150!important;
  background:#0c1017!important;
  box-shadow:0 8px 22px #0005!important;
}
.action-section-title{
  padding:10px 13px!important;
  font-family:Georgia,"Times New Roman",serif!important;
  font-size:1.08rem!important;
  font-weight:900!important;
  color:#fff3df!important;
}
.attack-section{border-color:#a92532!important;background:linear-gradient(180deg,#3a0d13,#130b0e)!important}
.attack-section .action-section-title{background:linear-gradient(90deg,#8d101b,#4c0c12)!important}
.regen-section{border-color:#268452!important;background:linear-gradient(180deg,#0a341f,#09130e)!important}
.regen-section .action-section-title{background:linear-gradient(90deg,#11613a,#0d3524)!important}
.discard-section{border-color:#7356b8!important;background:linear-gradient(180deg,#28194e,#100d1b)!important}
.discard-section .action-section-title{background:linear-gradient(90deg,#4b2d83,#2b1b50)!important}
.defense-section{border-color:#5f6d87!important;background:linear-gradient(180deg,#17202e,#0c1017)!important}
.defense-section .action-section-title{background:linear-gradient(90deg,#34425a,#202b3c)!important}
.other-section{border-color:#575d6c!important;background:#10131a!important}
.other-section .action-section-title{background:#242936!important}
.drawer-group-hand{
  display:grid!important;
  grid-template-columns:repeat(2,minmax(0,1fr))!important;
  gap:10px!important;
  width:100%!important;
  padding:10px!important;
  margin:0!important;
  overflow:visible!important;
  scroll-snap-type:none!important;
}
.drawer-group-hand .hand-card{width:100%!important;min-width:0!important;max-width:none!important;flex:none!important;margin:0!important}
.drawer-group-hand .hand-card img{display:block!important;width:100%!important;height:auto!important;aspect-ratio:63/88!important;object-fit:cover!important;border-radius:10px!important}
.drawer-group-hand .cardtag{display:none!important}
.discard-section .drawer-actions,.regen-section .drawer-actions{margin:0!important;padding:10px!important;display:block!important}
.discard-section #exchangeBtn{
  width:100%!important;
  margin:0!important;
  padding:13px 12px!important;
  border:1px solid #8f73ce!important;
  background:linear-gradient(180deg,#5a3890,#38235f)!important;
  color:#fff4e4!important;
  font-weight:800!important;
}
.regen-section #manfredBtn{
  width:100%!important;
  margin:0!important;
  border-color:#3f9f6d!important;
  background:linear-gradient(180deg,#176641,#0f442d)!important;
}
@media(min-width:620px){.drawer-group-hand{grid-template-columns:repeat(3,minmax(0,1fr))!important}}
@media(max-width:430px){
  .drawer-help{padding:10px!important}
  .drawer-help-title{font-size:.98rem!important}
  .drawer-help .action-option{min-height:52px!important;padding:9px 11px!important}
  .drawer-help .action-key{font-size:1.02rem!important}
  .drawer-help .action-detail{font-size:.86rem!important}
  .drawer-choice-title{font-size:1.2rem!important}
  .action-section-title{font-size:1rem!important;padding:9px 11px!important}
  .drawer-group-hand{gap:8px!important;padding:8px!important}
}
</style>
'''
css568_pattern = re.compile(r'<style id="v568-action-drawer">.*?</style>', re.S)
if css568_pattern.search(text):
    text = css568_pattern.sub(css568.strip(), text, count=1)
else:
    text = text.replace('</head>', css568 + '\n</head>', 1)

path.write_text(text, encoding='utf-8')
