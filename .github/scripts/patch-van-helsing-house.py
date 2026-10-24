from pathlib import Path
import re

PATH = Path('jeu-vampires-de-sarrebruck/index.html')
s = PATH.read_text(encoding='utf-8')
original = s
changes = []


def replace(old, new, label, required=True):
    global s
    count = s.count(old)
    if count == 0:
        if required:
            raise SystemExit(f'Motif introuvable: {label}')
        return 0
    s = s.replace(old, new)
    changes.append(f'{label}: {count}')
    return count


# Build marker: force le navigateur à distinguer clairement cette révision.
s, n = re.subn(
    r'<meta name="game-build" content="[^"]+">',
    '<meta name="game-build" content="20261024-helsing-house-v2">',
    s,
    count=1,
)
if n != 1:
    raise SystemExit('Meta game-build introuvable')
changes.append('game-build: 1')

# Ne jamais afficher les notes techniques de réglage au joueur.
technical_notes = [
    'Recherche volontaire : un objet garanti. Sans aucune munition, tu trouves un carreau d’argent.',
    'Fin de tour : 20 % de chance de trouver un objet. Répartition des objets trouvés : 55 % carreau · 25 % balle · 10 % pieu · 9 % sacoche · 1 % élixir. Noël donne toujours deux objets si la réserve n’est pas pleine.',
]
for note in technical_notes:
    count = s.count(note)
    if count:
        s = s.replace(note, '')
        changes.append(f'note technique supprimée: {count}')

# Équipement de départ : minimum identique à tous les niveaux.
s, n = re.subn(
    r'initial:\{silverBolts:\d+,blessedBullets:\d+,',
    'initial:{silverBolts:3,blessedBullets:2,',
    s,
    count=1,
)
if n != 1:
    raise SystemExit('Réglage initial Van Helsing introuvable')
changes.append('départ 3 carreaux / 2 balles: 1')

# Le seul bouton de recherche visible doit être celui DANS la maison / le tiroir d’équipement.
replace(
    "<button type=\"button\" class=\"helsing-search-action\" id=\"helsingResupplyBtn\" "+"(secretPowerAvailable(p,'van_helsing_resupply')?'':'disabled')+\">Rechercher des munitions — termine le tour</button>",
    "<button type=\"button\" class=\"helsing-search-action\" id=\"helsingResupplyBtn\" "+"(secretPowerAvailable(p,'van_helsing_resupply')?'':'disabled')+\">Rechercher des munitions</button>",
    'libellé rechercher des munitions',
)
replace(
    "if(search){search.classList.toggle('hidden',!isVanHelsing(h)||!h.alive||S.gameOver);search.disabled=!secretPowerAvailable(h,'van_helsing_resupply');}",
    "if(search){search.classList.add('hidden');search.disabled=true;}",
    'bouton flottant extérieur masqué',
)

# La fenêtre de recherche reste narrative : aucune statistique interne n’est montrée.
replace(
    "const ok=await openModal({title:'Rechercher des munitions',text:'Tu renonces à ton action pour chercher un objet garanti. Sans aucune munition, tu trouves un carreau d’argent. Cette recherche termine ton tour.',buttons:[{label:'Chercher',value:true},{label:'Retour',value:false}],closable:true});",
    "const ok=await openModal({title:'Rechercher des munitions',text:'Tu consacres ton action à fouiller les environs. Cette recherche termine ton tour.',buttons:[{label:'Chercher',value:true},{label:'Retour',value:false}],closable:true});",
    'fenêtre de recherche simplifiée',
)
replace(
    "const text=found?'Au coin d’une rue, tu as trouvé '+found.label+'. Cet objet rejoint tes réserves.':'Tu fouilles les environs, mais tu ne trouves aucune fourniture à emporter cette fois.';",
    "const text=found?'Au coin d’une rue, tu as trouvé '+found.label+'. Cet objet rejoint tes réserves.':'Tu fouilles les environs, mais tu ne trouves rien à emporter cette fois.';",
    'message aucune trouvaille',
)
replace(
    "if(!found)log('Cette fois, tu ne trouves aucune fourniture.','important');",
    "if(!found)log('Cette fois, tu ne trouves rien à emporter.','important');",
    'journal aucune trouvaille',
)
replace(
    "if(!options.length){log('Ta réserve de fournitures est pleine.');return null;}",
    "if(!options.length){log('Ta réserve de munitions et d’objets est pleine.');return null;}",
    'journal réserve pleine',
)

# Fouet, miroir et chapelet : réutilisables sans limite.
replace(
    "if(id==='van_helsing_rosary')return p.rosaryCharges>0?'':p.initialRosaryCharges===0?'Chapelet non fourni avec cet équipement de départ.':'Le chapelet n’a plus d’utilisation disponible.';",
    "if(id==='van_helsing_rosary')return '';",
    'chapelet toujours disponible',
)
replace(
    "if(id==='van_helsing_mirror')return p.mirrorCharges>0?'':p.initialMirrorCharges===0?'Miroir non fourni avec cet équipement de départ.':'Le miroir n’a plus d’utilisation disponible.';",
    "if(id==='van_helsing_mirror')return '';",
    'miroir toujours disponible',
)
replace(
    "(target.rosaryCharges||0)>0&&!uncounterable&&!isWolf(id)&&!CARDS[id]?.unblockable",
    "!uncounterable&&!isWolf(id)&&!CARDS[id]?.unblockable",
    'défense chapelet illimitée',
)
replace(
    "(target.mirrorCharges||0)>0&&!uncounterable&&!isWolf(id)&&!CARDS[id]?.unblockable",
    "!uncounterable&&!isWolf(id)&&!CARDS[id]?.unblockable",
    'défense miroir illimitée',
)
replace(
    "if(id==='van_helsing_mirror')return 'Annule cette attaque défendable et retire 1 goutte à l’attaquant, horrifié de ne pas voir son reflet. Utilisations limitées selon la difficulté.';",
    "if(id==='van_helsing_mirror')return 'Annule cette attaque défendable et retire 1 goutte à l’attaquant, horrifié de ne pas voir son reflet. Utilisations illimitées.';",
    'texte miroir illimité',
)
replace(
    "if(id==='van_helsing_rosary')return 'Présente le chapelet au vampire : son attaque est entièrement annulée. Consomme 1 utilisation disponible, sans défausser de carte ni utiliser ton action du tour.';",
    "if(id==='van_helsing_rosary')return 'Présente le chapelet au vampire : son attaque est entièrement annulée. Utilisations illimitées, sans défausser de carte ni utiliser ton action du tour.';",
    'texte chapelet illimité',
)

# Vérifications de sécurité : les fenêtres de fin de tour doivent rester branchées.
required = {
    'recherche Van Helsing en fin de tour': "if(p.alive&&drawAfter&&isVanHelsing(p)){await recoverHelsingTurnSupplies(p);}",
    'pioche vampire en fin de tour': "await drawOneToHand(p,p.human?'endturn':'normal');",
    'révélation visuelle de la pioche humaine': "const revealDraw=p.human&&(reason==='endturn'||reason==='exchange'||reason==='witchesBonus'||reason==='marche_noel');",
    'fenêtre résultat recherche Van Helsing': "await openModal({title:found?'Une trouvaille dans les parages !':'Recherche dans les environs'",
    'bouton recherche dans la maison': 'id="helsingResupplyBtn"',
    '3 carreaux au départ': 'initial:{silverBolts:3,blessedBullets:2,',
    'fouet illimité': "['consecratedWhipBtn','van_helsing_whip','Fouet consacré','Utilisations illimitées'",
    'miroir illimité affiché': "['mirrorInfoBtn','van_helsing_mirror','Miroir d’Erzulie Freda','Utilisations illimitées'",
    'chapelet illimité affiché': "['rosaryInfoBtn','van_helsing_rosary','Chapelet de sainte Marguerite','Utilisations illimitées'",
}
for label, needle in required.items():
    if needle not in s:
        raise SystemExit(f'Verification echouee: {label}')

if s == original:
    raise SystemExit('Aucune modification produite')

PATH.write_text(s, encoding='utf-8')
print('Patch Van Helsing appliqué :')
for change in changes:
    print(' -', change)
print('Vérifications de fin de tour et équipement : OK')
