from typing import List, Optional
from datetime import datetime
from .Recherche import Recherche


class RechercheEspace:
    def __init__(self, id: int, subject: str, objectif: str, date_time: str, bdd: "Bdd"):
        self.id = id
        self.subject = subject
        self.objectif = objectif
        self.date_time = date_time
        self.bdd = bdd

    @classmethod
    def create(cls, subject: str, objectif: str, bdd: "Bdd") -> "RechercheEspace":
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        bdd.cursor.execute('''
            INSERT INTO recherche_espaces (subject, date_time, objectif)
            VALUES (%s, %s, %s)
            RETURNING id
        ''', (subject, date_time, objectif))
        id_espace = bdd.cursor.fetchone()[0]
        bdd.conn.commit()
        return cls(id_espace, subject, objectif, date_time, bdd)


    @classmethod
    def load(cls, id_espace: int, bdd: "Bdd") -> Optional["RechercheEspace"]:
        # Charge l'espace depuis la base
        bdd.cursor.execute('''
            SELECT subject, date_time, objectif FROM recherche_espaces WHERE id = %s
        ''', (id_espace,))
        row = bdd.cursor.fetchone()
        if row:
            subject, date_time, objectif = row
            return cls(id_espace, subject, objectif, date_time, bdd)
        else:
            return None

    def __str__(self) -> str:
        return f"RechercheEspace(id={self.id}, subject='{self.subject}', objectif='{self.objectif}', date_time='{self.date_time}')"

    def dico(self) -> dict :
        return {
            "id": self.id,
            "subject": self.subject,
            "objectif": self.objectif,
            "date_time": self.date_time
        }

    def create_recherche(self, prompt: str, response: str) -> "Recherche":
        # Cr�e une recherche et la lie � cet espace
        # (� adapter selon ta m�thode de cr�ation de recherche)
        recherche = Recherche.create(self.id, prompt, response, self.bdd)
        # La liaison est d�j� faite dans la m�thode create de Recherche
        return recherche

    def get_recherches(self) -> List["Recherche"]:
        # R�cup�re les IDs des recherches associ�es � cet espace
        self.bdd.cursor.execute('''
            SELECT id_recherche FROM recherche_espace WHERE id_espace = %s
        ''', (self.id,))
        ids = [row[0] for row in self.bdd.cursor.fetchall()]
        recherches = []
        for id in ids:
            recherche = Recherche.load(id, self.bdd)
            if recherche is not None:
                recherches.append(recherche)
        return recherches

    def supprimer(self) -> bool:
        """
        Supprime l'espace de recherche et toutes ses recherches (et leurs �l�ments li�s).
        Retourne True si la suppression a r�ussi, False sinon.
        """
        try:
            # 1. R�cup�re toutes les recherches de cet espace
            recherches = self.get_recherches()

            # 2. Supprime chaque recherche (et ses �l�ments li�s)
            for recherche in recherches:
                if not recherche.supprimer():  # Utilise la m�thode supprimer de la classe Recherche
                    print(f"Erreur lors de la suppression de la recherche {recherche.id}")
                    # On pourrait choisir de continuer ou d'arr�ter ici

            # 3. Supprime l'espace de recherche lui-m�me
            self.bdd.cursor.execute('DELETE FROM recherche_espaces WHERE id = %s', (self.id,))
            self.bdd.conn.commit()
            return True
        except Exception as e:
            print(f"Erreur lors de la suppression de l'espace {self.id} : {e}")
            self.bdd.conn.rollback()
            return False
        
