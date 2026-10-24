from pathlib import Path
import re

PATH = Path('jeu-vampires-de-sarrebruck/index.html')
s = PATH.read_text(encoding='utf-8')
original = s

technical_notes = [
    'Recherche volontaire : un objet garanti. Sans aucune munition, tu trouves un carreau d’argent.',
    'Fin de tour : 20 % de chance de trouver un objet. Répartition des objets trouvés : 55 % carreau · 25 % balle · 10 % pieu · 9 % sacoche · 1 % élixir. Noël donne toujours deux objets si la réserve n’est pas pleine.',
]

# Marqueur de version pour distinguer clairement cette révision.
s, n = re.subn(
    r'<meta name="game-build" content="[^"]+">',
    '<meta name="game-build" content="20261024-helsing-house-v3">',
    s,
    count=1,
)
if n != 1:
    raise SystemExit('Meta game-build introuvable')

# Les réglages internes ne doivent jamais être affichés au joueur.
for note in technical_notes:
    s = s.replace(note, '')

# Équipement de départ identique au minimum demandé, quelle que soit la difficulté.
s, n = re.subn(
    r'initial:\{silverBolts:\d+,blessedBullets:\d+,',
    'initial:{silverBolts:3,blessedBullets:2,',
    s,
    count=1,
)
if n != 1:
    raise SystemExit('Réglage initial Van Helsing introuvable')

# Le bouton de recherche doit être dans le tiroir / la maison, et uniquement là.
s = s.replace(
    '>Rechercher des munitions — termine le tour</button>',
    '>Rechercher des munitions</button>',
)
s = s.replace(
    "if(search){search.classList.toggle('hidden',!isVanHelsing(h)||!h.alive||S.gameOver);search.disabled=!secretPowerAvailable(h,'van_helsing_resupply');}",
    "if(search){search.classList.add('hidden');search.disabled=true;}",
)

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
    'libellé Rechercher des munitions': '>Rechercher des munitions</button>',
    'bouton flottant extérieur masqué': "if(search){search.classList.add('hidden');search.disabled=true;}",
    'départ avec 3 carreaux et 2 balles': 'initial:{silverBolts:3,blessedBullets:2,',
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
print('Correctif Van Helsing validé : maison, équipement et fins de tour OK.')
