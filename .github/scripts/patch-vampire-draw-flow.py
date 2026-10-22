from pathlib import Path

path = Path('jeu-vampires-de-sarrebruck/index.html')
text = path.read_text(encoding='utf-8')

# 1) Marché de Noël : ne jamais révéler les cartes piochées par les IA.
old = "const revealDraw=(p.human&&(reason==='endturn'||reason==='exchange'||reason==='witchesBonus'||reason==='marche_noel'))||(reason==='marche_noel'&&CARDS[id].kind==='immediate');"
new = "const revealDraw=p.human&&(reason==='endturn'||reason==='exchange'||reason==='witchesBonus'||reason==='marche_noel');"
if old not in text:
    raise SystemExit('revealDraw pattern not found')
text = text.replace(old, new, 1)

# 2) Texte court validé pour une carte à effet immédiat.
old = '? "⚡ Regarde bien la carte : son effet s’appliquera lorsque tu continueras."'
new = '? "Effet immédiat : applique l’action de cette carte maintenant."'
if old not in text:
    raise SystemExit('immediate info pattern not found')
text = text.replace(old, new, 1)

# Supprime la répétition sous le texte principal pour les cartes immédiates.
old = '<div class="scene-small">${immediate?"Son effet se déclenchera quand tu continueras.":"La carte rejoint ta main."}</div>'
new = '<div class="scene-small">${immediate?"":"La carte rejoint ta main."}</div>'
if old not in text:
    raise SystemExit('scene-small pattern not found')
text = text.replace(old, new, 1)

# 3) Petite transition explicative avant la repioche.
anchor = "async function drawOneToHand(p,reason='normal'){"
helper = """async function showImmediateRepickNotice(){
 const content=`<div class=\"immediate-repick-notice\"><div class=\"immediate-repick-icon\">✦</div><div><strong>Effet immédiat effectué</strong><span>Tu repioches.</span></div><div class=\"tap-dismiss-note\">Touche pour continuer</div></div>`;
 await openTapDismissInfo({title:'',content});
}
"""
if helper not in text:
    if anchor not in text:
        raise SystemExit('drawOneToHand anchor not found')
    text = text.replace(anchor, helper + anchor, 1)

old = "await resolveImmediate(p,id,{skipScene:true,drawReason:reason});\n     if(S!==game||game.gameOver)return null;\n     if(id!=='sorcieres'||!p.witches)discardCard(id);render();if(!p.alive)return null;continue;"
new = "await resolveImmediate(p,id,{skipScene:true,drawReason:reason});\n     if(S!==game||game.gameOver)return null;\n     if(revealDraw&&p.human&&p.alive)await showImmediateRepickNotice();\n     if(S!==game||game.gameOver)return null;\n     if(id!=='sorcieres'||!p.witches)discardCard(id);render();if(!p.alive)return null;continue;"
if old not in text:
    raise SystemExit('resolveImmediate continuation pattern not found')
text = text.replace(old, new, 1)

# Style discret de la transition.
css = """
<style id=\"v571-immediate-repick\">
.immediate-repick-notice{
  display:flex;flex-direction:column;align-items:center;justify-content:center;
  gap:12px;text-align:center;padding:28px 18px 22px;min-height:210px;
}
.immediate-repick-icon{font-size:2.15rem;color:#e8c678;line-height:1}
.immediate-repick-notice strong{display:block;font-family:Georgia,serif;font-size:1.6rem;color:#f3e4c8;margin-bottom:8px}
.immediate-repick-notice span{display:block;font-size:1.28rem;font-weight:800;color:#fff}
.immediate-repick-notice .tap-dismiss-note{margin-top:14px;font-size:.9rem;opacity:.72}
</style>
"""
if 'id="v571-immediate-repick"' not in text:
    if '</head>' not in text:
        raise SystemExit('head close not found')
    text = text.replace('</head>', css + '\n</head>', 1)

path.write_text(text, encoding='utf-8')
print('Draw flow patched successfully')
