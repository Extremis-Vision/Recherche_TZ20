from BDD.BDD import Bdd
from BDD.MotCle import MotCle

bdd = Bdd()

listes_mots = bdd.get_MotCle()

for mot in listes_mots:
    print(mot)
    print(mot.supprimer(bdd))

