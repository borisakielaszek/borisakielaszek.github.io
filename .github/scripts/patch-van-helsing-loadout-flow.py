from pathlib import Path
import re

path = Path('jeu-vampires-de-sarrebruck/index.html')
text = path.read_text(encoding='utf-8')
original = text

# 1) Van Helsing always starts with at least 3 silver bolts and 2 blessed bullets,
# independently of difficulty / opponent count.
old = "Object.assign(human,balance.initial);human.initialRosaryCharges=human.rosaryCharges;human.initialMirrorCharges=human.mirrorCharges;"
new = "Object.assign(human,balance.initial);human.silverBolts=Math.max(3,human.silverBolts||0);human.blessedBullets=Math.max(2,human.blessedBullets||0);human.initialRosaryCharges=human.rosaryCharges;human.initialMirrorCharges=human.mirrorCharges;"
if old not in text:
    raise SystemExit('Van Helsing initial loadout anchor not found')
text = text.replace(old, new, 1)

# 2) Manual search button in the hand: short, explicit label.
old = ">Rechercher des munitions — termine le tour</button>"
new = ">Rechercher des munitions</button>"
if old not in text:
    raise SystemExit('Van Helsing resupply button label not found')
text = text.replace(old, new, 1)

# Keep the confirmation useful, but do not expose balancing / guarantee mechanics.
old = "const ok=await openModal({title:'Rechercher des munitions',text:'Tu renonces à ton action pour chercher un objet garanti. Sans aucune munition, tu trouves un carreau d’argent. Cette recherche termine ton tour.',buttons:[{label:'Chercher',value:true},{label:'Retour',value:false}],closable:true});"
new = "const ok=await openModal({title:'Rechercher des munitions',text:'Tu consacres ton action à fouiller les environs. Cette recherche termine ton tour.',buttons:[{label:'Chercher',value:true},{label:'Retour',value:false}],closable:true});"
if old not in text:
    raise SystemExit('Van Helsing resupply confirmation text not found')
text = text.replace(old, new, 1)

# 3) Mirror and rosary are genuinely unlimited defenses.
old = "(target.rosaryCharges||0)>0&&!uncounterable&&!isWolf(id)&&!CARDS[id]?.unblockable);"
new = "!uncounterable&&!isWolf(id)&&!CARDS[id]?.unblockable);"
if old not in text:
    raise SystemExit('Rosary availability condition not found')
text = text.replace(old, new, 1)

old = "(target.mirrorCharges||0)>0&&!uncounterable&&!isWolf(id)&&!CARDS[id]?.unblockable);"
new = "!uncounterable&&!isWolf(id)&&!CARDS[id]?.unblockable);"
if old not in text:
    raise SystemExit('Mirror availability condition not found')
text = text.replace(old, new, 1)

old = "if(id==='van_helsing_rosary')return p.rosaryCharges>0?'':p.initialRosaryCharges===0?'Chapelet non fourni avec cet équipement de départ.':'Le chapelet n’a plus d’utilisation disponible.';"
new = "if(id==='van_helsing_rosary')return '';"
if old not in text:
    raise SystemExit('Rosary unavailable reason not found')
text = text.replace(old, new, 1)

old = "if(id==='van_helsing_mirror')return p.mirrorCharges>0?'':p.initialMirrorCharges===0?'Miroir non fourni avec cet équipement de départ.':'Le miroir n’a plus d’utilisation disponible.';"
new = "if(id==='van_helsing_mirror')return '';"
if old not in text:
    raise SystemExit('Mirror unavailable reason not found')
text = text.replace(old, new, 1)

old = "if(id==='van_helsing_mirror')return 'Annule cette attaque défendable et retire 1 goutte à l’attaquant, horrifié de ne pas voir son reflet. Utilisations limitées selon la difficulté.';"
new = "if(id==='van_helsing_mirror')return 'Annule cette attaque défendable et retire 1 goutte à l’attaquant, horrifié de ne pas voir son reflet. Utilisations illimitées.';"
if old not in text:
    raise SystemExit('Mirror defense copy not found')
text = text.replace(old, new, 1)

old = "if(id==='van_helsing_rosary')return 'Présente le chapelet au vampire : son attaque est entièrement annulée. Consomme 1 utilisation disponible, sans défausser de carte ni utiliser ton action du tour.';"
new = "if(id==='van_helsing_rosary')return 'Présente le chapelet au vampire : son attaque est entièrement annulée. Utilisations illimitées, sans défausser de carte ni utiliser ton action du tour.';"
if old not in text:
    raise SystemExit('Rosary defense copy not found')
text = text.replace(old, new, 1)

# 4) Remove balancing notes accidentally exposed in the Van Helsing house/equipment UI.
# Their mechanics remain in the game code; only the technical explanatory copy disappears.
patterns = [
    r'<(?P<tag>p|div|li)(?P<attrs>[^>]*)>\s*Recherche volontaire\s*:\s*.*?</(?P=tag)>',
    r'<(?P<tag>p|div|li)(?P<attrs>[^>]*)>\s*Fin de tour\s*:\s*20\s*%.*?</(?P=tag)>',
]
for pattern in patterns:
    text = re.sub(pattern, '', text, flags=re.IGNORECASE | re.DOTALL)

# 5) Force the hand search control to stay visible even if older responsive rules hide buttons.
style = r'''
<style id="v575-helsing-search-loadout">
#humanPanel .helsing-search-action,
.card-drawer .helsing-search-action,
.helsing-search-action{
  display:block!important;
  visibility:visible!important;
  opacity:1!important;
  width:min(100%,520px)!important;
  margin:12px auto 18px!important;
}
</style>
'''
if 'id="v575-helsing-search-loadout"' not in text:
    if '</head>' not in text:
        raise SystemExit('head close not found')
    text = text.replace('</head>', style + '\n</head>', 1)

if text == original:
    raise SystemExit('No changes made')

path.write_text(text, encoding='utf-8')
print('Van Helsing loadout and end-turn search flow patched successfully')
