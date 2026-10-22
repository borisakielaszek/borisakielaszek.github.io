from pathlib import Path

p = Path('jeu-vampires-de-sarrebruck/index.html')
s = p.read_text(encoding='utf-8')

old1 = "`${p.human?'Tu as':pName(p)+' a'} tiré Hexennacht. Tous les vampires vont maintenant voler 1 carte face cachée à leur voisin de droite. Quand ce sera ton tour, le jeu te montrera les cartes de ton voisin.`"
new1 = "`${player.human?'Tu as':pName(player)+' a'} tiré Hexennacht. Tous les vampires vont maintenant voler 1 carte face cachée à leur voisin de droite. Quand ce sera ton tour, le jeu te montrera les cartes de ton voisin.`"

old2 = "`🎁 ${p.human?'Tu as':pName(p)+' a'} tiré le Marché de Noël : cadeau pour tout le monde ! Chaque vampire va piocher 2 nouvelles cartes dans la pioche commune.`"
new2 = "`🎁 ${player.human?'Tu as':pName(player)+' a'} tiré le Marché de Noël : cadeau pour tout le monde ! Chaque vampire va piocher 2 nouvelles cartes dans la pioche commune.`"

changed = False
for old, new in ((old1, new1), (old2, new2)):
    if old in s:
        s = s.replace(old, new, 1)
        changed = True

if not changed:
    # Already fixed is acceptable; otherwise fail loudly if neither the old nor corrected forms exist.
    if new1 not in s or new2 not in s:
        raise SystemExit('End-turn reveal patch targets not found')

p.write_text(s, encoding='utf-8')
