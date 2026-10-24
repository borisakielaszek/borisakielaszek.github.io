from pathlib import Path
import re

PATH = Path('jeu-vampires-de-sarrebruck/index.html')
s = PATH.read_text(encoding='utf-8')
original = s

# Nouvelle version : Van Helsing dispose enfin d'un soin dès le départ
# et les objets de régénération restent trouvables en fin de tour.
s, n = re.subn(
    r'<meta name="game-build" content="[^"]+">',
    '<meta name="game-build" content="20261024-helsing-healing-v5">',
    s,
    count=1,
)
if n != 1:
    raise SystemExit('Meta game-build introuvable')

# Équipement de départ : 3 carreaux, 2 balles, 1 pieu et 1 sacoche de soins.
old_initial = 'initial:{silverBolts:3,blessedBullets:2,gepettoStakes:1,medkitUses:0,elixirDoses:0,rosaryCharges:1,mirrorCharges:1}'
new_initial = 'initial:{silverBolts:3,blessedBullets:2,gepettoStakes:1,medkitUses:1,elixirDoses:0,rosaryCharges:1,mirrorCharges:1}'
if old_initial in s:
    s = s.replace(old_initial, new_initial, 1)
elif new_initial not in s:
    raise SystemExit('Réglage initial Van Helsing introuvable')

# Trouvailles : 53 % carreau, 25 % balle, 10 % pieu, 10 % sacoche, 2 % élixir.
# Les cinq valeurs totalisent 100 et sont utilisées uniquement lorsqu'une trouvaille a lieu.
s, n = re.subn(
    r'weights:\[\s*\d+\s*,\s*\d+\s*,\s*\d+\s*,\s*\d+\s*,\s*\d+\s*\]',
    'weights:[53,25,10,10,2]',
    s,
    count=1,
)
if n != 1:
    raise SystemExit('Pondération des trouvailles Van Helsing introuvable')

required = {
    'sacoche de départ': 'medkitUses:1,elixirDoses:0',
    'pondération soins': 'weights:[53,25,10,10,2]',
    'sacoche trouvable': "medkitUses:{label:'une sacoche médicale'",
    'élixir trouvable': "elixirDoses:{label:'une dose d’élixir de survie'",
    'recherche de fin de tour': 'await recoverHelsingTurnSupplies(p);',
    'sacoche utilisable': 'async function useHelsingMedkit()',
    'élixir utilisable': 'async function useHelsingElixir()',
}
for label, needle in required.items():
    if needle not in s:
        raise SystemExit(f'Verification echouee: {label}')

if s == original:
    raise SystemExit('Aucune modification produite')

PATH.write_text(s, encoding='utf-8')
print('Correctif Van Helsing v5 : 1 sacoche au départ, sacoches et élixirs trouvables en fin de tour.')
