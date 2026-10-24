from pathlib import Path
import re

PATH = Path('jeu-vampires-de-sarrebruck/index.html')
s = PATH.read_text(encoding='utf-8')
original = s

technical_notes = [
    'Recherche volontaire : un objet garanti. Sans aucune munition, tu trouves un carreau d’argent.',
    'Fin de tour : 20 % de chance de trouver un objet. Répartition des objets trouvés : 55 % carreau · 25 % balle · 10 % pieu · 9 % sacoche · 1 % élixir.',
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

# Libellé clair du bouton dans l’arsenal, quelle que soit la forme de chaîne utilisée.
s = s.replace('Rechercher des munitions — termine le tour', 'Chercher des munitions à proximité')
s = s.replace('Rechercher des munitions', 'Chercher des munitions à proximité')

# Le vieux bouton flottant extérieur reste masqué : la recherche doit être dans l’arsenal.
s = s.replace(
    "if(search){search.classList.toggle('hidden',!isVanHelsing(h)||!h.alive||S.gameOver);search.disabled=!secretPowerAvailable(h,'van_helsing_resupply');}",
    "if(search){search.classList.add('hidden');search.disabled=true;}",
)

# Sur mobile, une ancienne règle responsive pouvait masquer le conteneur parent.
# On force donc le panneau COMPLET à rester affiché, juste après les compteurs de munitions.
mobile_style = r'''
<style id="v576-helsing-search-panel-mobile">
#humanPanel .helsing-search-panel,
.card-drawer .helsing-search-panel,
.helsing-search-panel{
  display:block!important;
  visibility:visible!important;
  opacity:1!important;
  position:relative!important;
  z-index:5!important;
  width:100%!important;
  max-width:560px!important;
  margin:14px auto 18px!important;
}
#humanPanel .helsing-search-action,
.card-drawer .helsing-search-action,
.helsing-search-action{
  display:block!important;
  visibility:visible!important;
  width:100%!important;
  min-height:54px!important;
}
.helsing-search-action:disabled{opacity:.45!important;}
</style>
'''
if 'id="v576-helsing-search-panel-mobile"' not in s:
    if '</head>' not in s:
        raise SystemExit('Fermeture head introuvable')
    s = s.replace('</head>', mobile_style + '\n</head>', 1)

# Nettoyage des formulations résiduelles destinées au réglage interne.
s = s.replace('aucune fourniture à emporter cette fois', 'rien à emporter cette fois')
s = s.replace('Cette fois, tu ne trouves aucune fourniture.', 'Cette fois, tu ne trouves rien à emporter.')
s = s.replace('Ta réserve de fournitures est pleine.', 'Ta réserve de munitions et d’objets est pleine.')
s = s.replace('Utilisations limitées selon la difficulté.', 'Utilisations illimitées.')
s = s.replace(
    'Consomme 1 utilisation disponible, sans défausser de carte ni utiliser ton action du tour.',
    'Utilisations illimitées, sans défausser de carte ni utiliser ton action du tour.',
)

required = {
    'bouton de recherche dans la maison': 'id="helsingResupplyBtn"',
    'libellé Chercher des munitions à proximité': 'Chercher des munitions à proximité',
    'panneau mobile forcé visible': 'id="v576-helsing-search-panel-mobile"',
    'panneau placé juste après les munitions': 'summary.innerHTML=ammoHTML+searchHTML+secretPowersHTML(p);',
    'bouton flottant extérieur masqué': "if(search){search.classList.add('hidden');search.disabled=true;}",
    'départ 3 carreaux, 2 balles, 1 pieu': 'initial:{silverBolts:3,blessedBullets:2,gepettoStakes:1,',
    'minimum runtime 1 pieu': 'human.gepettoStakes=Math.max(1,human.gepettoStakes||0);',
    'recherche Van Helsing de fin de tour': "if(p.alive&&drawAfter&&isVanHelsing(p)){await recoverHelsingTurnSupplies(p);}",
    'pioche vampire de fin de tour': "await drawOneToHand(p,p.human?'endturn':'normal');",
    'fenêtre visuelle de pioche': "const revealDraw=p.human&&(reason==='endturn'||reason==='exchange'||reason==='witchesBonus'||reason==='marche_noel');",
    'fenêtre résultat de recherche': "await openModal({title:found?'Une trouvaille dans les parages !':'Recherche dans les environs'",
    'fouet illimité': "['consecratedWhipBtn','van_helsing_whip','Fouet consacré','Utilisations illimitées'",
    'miroir illimité': "['mirrorInfoBtn','van_helsing_mirror','Miroir d’Erzulie Freda','Utilisations illimitées'",
    'chapelet illimité': "['rosaryInfoBtn','van_helsing_rosary','Chapelet de sainte Marguerite','Utilisations illimitées'",
}
for label, needle in required.items():
    if needle not in s:
        raise SystemExit(f'Verification echouee: {label}')

for forbidden in technical_notes + [
    'Utilisations limitées selon la difficulté.',
    'Consomme 1 utilisation disponible',
]:
    if forbidden in s:
        raise SystemExit(f'Texte interdit encore présent: {forbidden}')

if s == original:
    raise SystemExit('Aucune modification produite')

PATH.write_text(s, encoding='utf-8')
print('Correctif Van Helsing v4 validé : bouton mobile visible et 1 pieu minimum.')
