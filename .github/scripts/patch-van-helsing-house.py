from pathlib import Path
import re

PATH = Path('jeu-vampires-de-sarrebruck/index.html')
s = PATH.read_text(encoding='utf-8')
original = s

technical_notes = [
    'Recherche volontaire : un objet garanti. Sans aucune munition, tu trouves un carreau d’argent.',
    'Fin de tour : 20 % de chance de trouver un objet. Répartition des objets trouvés : 55 % carreau · 25 % balle · 10 % pieu · 9 % sacoche · 1 % élixir. Noël donne toujours deux objets si la réserve n’est pas pleine.',
]

# Marqueur de version.
s, n = re.subn(
    r'<meta name="game-build" content="[^"]+">',
    '<meta name="game-build" content="20261024-helsing-house-v4">',
    s,
    count=1,
)
if n != 1:
    raise SystemExit('Meta game-build introuvable')

# Les réglages internes ne doivent jamais être affichés au joueur.
for note in technical_notes:
    s = s.replace(note, '')

# Équipement de départ minimum identique à toutes les difficultés.
s, n = re.subn(
    r'initial:\{silverBolts:\d+,blessedBullets:\d+,gepettoStakes:\d+,',
    'initial:{silverBolts:3,blessedBullets:2,gepettoStakes:1,',
    s,
    count=1,
)
if n != 1:
    raise SystemExit('Réglage initial Van Helsing introuvable')

# Renforce aussi le minimum au moment où Van Helsing est initialisé.
if 'human.gepettoStakes=Math.max(1,human.gepettoStakes||0);' not in s:
    s, n = re.subn(
        r'(human\.blessedBullets=Math\.max\(2,human\.blessedBullets\|\|0\);)',
        r'\1human.gepettoStakes=Math.max(1,human.gepettoStakes||0);',
        s,
        count=1,
    )
    if n != 1:
        raise SystemExit('Initialisation runtime Van Helsing introuvable')

# Libellé clair dans l'arsenal et dans sa fenêtre de confirmation.
s = s.replace('Rechercher des munitions — termine le tour', 'Chercher des munitions à proximité')
s = s.replace('Rechercher des munitions', 'Chercher des munitions à proximité')

# Le bouton de l'arsenal doit être réellement visible sur mobile, pas seulement présent dans le code.
button_anchor = '<button type="button" class="helsing-search-action" id="helsingResupplyBtn"'
button_visible = '<button type="button" class="helsing-search-action" id="helsingResupplyBtn" style="display:block!important;visibility:visible!important;width:calc(100% - 24px)!important;min-height:58px!important;margin:16px 12px 20px!important;position:relative!important;z-index:20!important"'
if button_visible not in s:
    if button_anchor not in s:
        raise SystemExit('Bouton de recherche Van Helsing introuvable')
    s = s.replace(button_anchor, button_visible, 1)

# Le vieux bouton flottant extérieur reste masqué : la recherche doit être dans l'arsenal.
s = s.replace(
    "if(search){search.classList.toggle('hidden',!isVanHelsing(h)||!h.alive||S.gameOver);search.disabled=!secretPowerAvailable(h,'van_helsing_resupply');}",
    "if(search){search.classList.add('hidden');search.disabled=true;}",
)

# Renfort CSS mobile en plus du style inline.
mobile_style = r'''
<style id="v576-helsing-search-panel-mobile">
#humanPanel .helsing-search-action,
.card-drawer .helsing-search-action,
.helsing-search-action{
  display:block!important;
  visibility:visible!important;
  width:calc(100% - 24px)!important;
  min-height:58px!important;
  margin:16px 12px 20px!important;
  position:relative!important;
  z-index:20!important;
}
.helsing-search-action:disabled{opacity:.45!important;}
</style>
'''
if 'id="v576-helsing-search-panel-mobile"' not in s:
    if '</head>' not in s:
        raise SystemExit('Fermeture head introuvable')
    s = s.replace('</head>', mobile_style + '\n</head>', 1)

# Nettoyage de formulations résiduelles.
s = s.replace('aucune fourniture à emporter cette fois', 'rien à emporter cette fois')
s = s.replace('Cette fois, tu ne trouves aucune fourniture.', 'Cette fois, tu ne trouves rien à emporter.')
s = s.replace('Ta réserve de fournitures est pleine.', 'Ta réserve de munitions et d’objets est pleine.')
s = s.replace('Utilisations limitées selon la difficulté.', 'Utilisations illimitées.')
s = s.replace(
    'Consomme 1 utilisation disponible, sans défausser de carte ni utiliser ton action du tour.',
    'Utilisations illimitées, sans défausser de carte ni utiliser ton action du tour.',
)

required = {
    'bouton de recherche dans l’arsenal': 'id="helsingResupplyBtn"',
    'libellé Chercher des munitions à proximité': 'Chercher des munitions à proximité',
    'style mobile forcé visible': 'id="v576-helsing-search-panel-mobile"',
    'style inline du bouton': 'min-height:58px!important',
    'bouton flottant extérieur masqué': "if(search){search.classList.add('hidden');search.disabled=true;}",
    'départ 3 carreaux, 2 balles, 1 pieu': 'initial:{silverBolts:3,blessedBullets:2,gepettoStakes:1,',
    'minimum runtime 1 pieu': 'human.gepettoStakes=Math.max(1,human.gepettoStakes||0);',
    'recherche Van Helsing de fin de tour': "if(p.alive&&drawAfter&&isVanHelsing(p)){await recoverHelsingTurnSupplies(p);}",
    'pioche vampire de fin de tour': "await drawOneToHand(p,p.human?'endturn':'normal');",
    'fenêtre résultat de recherche': "await openModal({title:found?'Une trouvaille dans les parages !':'Recherche dans les environs'",
}
for label, needle in required.items():
    if needle not in s:
        raise SystemExit(f'Verification echouee: {label}')

# Le bouton doit être entre la réserve de munitions et la première catégorie (Observation).
ammo_pos = s.find('class="helsing-ammo-summary"')
button_pos = s.find('id="helsingResupplyBtn"')
groups_pos = s.find("groups.map(([title,kind,ids])=>", button_pos)
if not (ammo_pos != -1 and button_pos != -1 and groups_pos != -1 and ammo_pos < button_pos < groups_pos):
    raise SystemExit('Verification echouee: position du bouton dans l’arsenal')

for forbidden in technical_notes + [
    'Utilisations limitées selon la difficulté.',
    'Consomme 1 utilisation disponible',
]:
    if forbidden in s:
        raise SystemExit(f'Texte interdit encore présent: {forbidden}')

if s == original:
    raise SystemExit('Aucune modification produite')

PATH.write_text(s, encoding='utf-8')
print('Correctif Van Helsing v4 validé : bouton mobile visible sous les munitions et 1 pieu minimum.')
