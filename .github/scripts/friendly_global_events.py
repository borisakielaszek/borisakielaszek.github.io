from pathlib import Path

p = Path('jeu-vampires-de-sarrebruck/index.html')
s = p.read_text(encoding='utf-8')

marker = "const IMMEDIATE_EXPLAIN={"
if marker not in s:
    anchor = "const CARD_EXPLAIN={"
    if anchor not in s:
        raise SystemExit('CARD_EXPLAIN anchor not found')
    block = """const IMMEDIATE_EXPLAIN={
 marche_noel:\"🎁 Cadeau de Noël pour tout le monde : chaque vampire pioche 2 nouvelles cartes dans la pioche commune. Si ta main dépasse sa limite, tu choisiras ensuite quoi défausser.\",
 hexennacht:\"La Nuit des sorcières entraîne toute la table : chaque vampire vole 1 carte face cachée à son voisin de droite.\",
 fossoyeur:\"Le Fossoyeur te fait perdre 1 goutte de sang.\",
 mortetrouille:\"Mortetrouille fouille la défausse : tu choisis 1 carte parmi les 5 dernières et tu appliques immédiatement son effet.\",
 monstre:\"Le monstre du Schafbach t’attaque : tu perds 2 gouttes de sang.\",
 proie_brandenbusch:\"Tu saignes une proie dans la forêt du Brandenbourg : tu récupères 2 gouttes de sang.\",
 proie_schalkenthal:\"Tu saignes une proie dans la forêt de Schalkenthal : tu récupères 1 goutte de sang.\",
 proie_bahnhof:\"Tu saignes une proie devant la gare centrale : tu récupères 1 goutte de sang et tu pioches 2 cartes supplémentaires.\",
 sorcieres:\"Les Sorcières d’Oeting s’installent à tes côtés : ta main maximale passe à 7 cartes et tu pioches immédiatement 1 carte supplémentaire.\",
 chute_sarre:\"Tu chutes dans la Sarre : tu dois défausser 1 carte puis passer ton prochain tour, sauf si un pouvoir ou une carte te permet d’éviter la chute.\",
 fleau:\"Le Fléau Purificateur frappe toute la table : chaque vampire perd 1 goutte de sang.\",
 fantome:\"Le Fantôme te demande de choisir un autre vampire : il reçoit 1 goutte de sang provenant de la réserve commune.\",
 peste:\"La peste frappe les vampires encore bien nourris : tous ceux qui ont au moins 4 gouttes de sang en perdent 2.\"
};

"""
    s = s.replace(anchor, block + anchor, 1)

old = ''' const info=immediate
   ? (id==='hexennacht'
      ? `${player.human?'Tu as':pName(player)+' a'} tiré Hexennacht. Tous les vampires vont maintenant voler 1 carte face cachée à leur voisin de droite. Quand ce sera ton tour, le jeu te montrera les cartes de ton voisin.`
      : id==='marche_noel'
      ? `🎁 ${player.human?'Tu as':pName(player)+' a'} tiré le Marché de Noël : cadeau pour tout le monde ! Chaque vampire va piocher 2 nouvelles cartes dans la pioche commune.`
      : \"Effet immédiat : l’action de cette carte se déclenche maintenant.\")
   : christmasDraw
   ? \"🎁 Cadeau de Noël ! Voici l’une des deux nouvelles cartes que tu reçois. Elle rejoint ta main. Après la seconde, si ta main est trop pleine, tu choisiras simplement quoi défausser.\"
   : (witchesBonus?\"Cette carte profite immédiatement de ta nouvelle main maximale de 7.\":\"Prends le temps de regarder la carte avant de continuer.\");
 const title=immediate&&id==='hexennacht'?\"🌙 Hexennacht — tout le monde participe\":immediate&&id==='marche_noel'?\"🎁 Marché de Noël — cadeaux pour tous\":christmasDraw?\"🎁 Marché de Noël — ton cadeau\":witchesBonus?\"Carte supplémentaire\":\"\";
 const content=`<div class=\"immediate-scene draw-scene\"><div class=\"scene-kicker draw-kicker\">${kicker}</div><img src=\"${imgCard(id)}\" alt=\"${cardName(id)}\"><div class=\"immediate-scene-copy\"><div class=\"scene-title\">${cardName(id)}</div><div class=\"scene-text\">${info}</div><div class=\"scene-small\">${immediate?\"\":\"La carte rejoint ta main.\"}</div><div class=\"tap-dismiss-note\">Touche cette notification pour continuer</div></div></div>`;'''

new = ''' const info=immediate
   ? \"Effet immédiat : applique l’action de cette carte maintenant.\"
   : christmasDraw
   ? \"🎁 Cadeau de Noël ! Voici l’une des deux nouvelles cartes que tu reçois. Elle rejoint ta main. Après la seconde, si ta main est trop pleine, tu choisiras simplement quoi défausser.\"
   : (witchesBonus?\"Cette carte profite immédiatement de ta nouvelle main maximale de 7.\":\"Prends le temps de regarder la carte avant de continuer.\");
 const effectDetail=immediate?(IMMEDIATE_EXPLAIN[id]||CARD_EXPLAIN[id]||\"L’effet indiqué sur la carte s’applique immédiatement.\"):\"\";
 const title=immediate&&id==='hexennacht'?\"🌙 Hexennacht — tout le monde participe\":immediate&&id==='marche_noel'?\"🎁 Marché de Noël — cadeaux pour tous\":christmasDraw?\"🎁 Marché de Noël — ton cadeau\":witchesBonus?\"Carte supplémentaire\":\"\";
 const content=`<div class=\"immediate-scene draw-scene\"><div class=\"scene-kicker draw-kicker\">${kicker}</div><img src=\"${imgCard(id)}\" alt=\"${cardName(id)}\"><div class=\"immediate-scene-copy\"><div class=\"scene-title\">${cardName(id)}</div><div class=\"scene-text\">${info}</div>${immediate?`<div class=\"scene-effect-detail\">${effectDetail}</div>`:\"\"}<div class=\"scene-small\">${immediate?\"\":\"La carte rejoint ta main.\"}</div><div class=\"tap-dismiss-note\">Touche cette notification pour continuer</div></div></div>`;'''

if old not in s:
    if 'const effectDetail=immediate?' not in s:
        raise SystemExit('showDrawScene block not found')
else:
    s = s.replace(old, new, 1)

style_marker = '.scene-effect-detail{'
if style_marker not in s:
    css = '''\n<style id=\"v574-immediate-effect-detail\">\n.scene-effect-detail{margin-top:12px;padding:11px 13px;border-radius:12px;background:#0b0d13cc;border:1px solid #6f5a3a;color:#f6ead6;font-family:system-ui,sans-serif;font-size:1rem;line-height:1.45;font-weight:650}\n@media(max-width:520px){.scene-effect-detail{font-size:.92rem;padding:10px 11px}}\n</style>\n'''
    s = s.replace('</head>', css + '</head>', 1)

p.write_text(s, encoding='utf-8')
