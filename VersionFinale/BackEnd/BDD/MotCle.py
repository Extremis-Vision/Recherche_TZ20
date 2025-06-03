from typing import Optional

class MotCle:
    def __init__(self, id: int, mot: str):
        self.id = id
        self.mot = mot

    @classmethod
    def create(cls,id_recherche : int, mot: str, bdd: "Bdd") -> "MotCle":
        bdd.cursor.execute('''
            INSERT INTO keywords (mot)
            VALUES (%s)
            RETURNING id
        ''', (mot,))
        id = bdd.cursor.fetchone()[0]
        bdd.conn.commit()
        bdd.cursor.execute('''
            INSERT INTO recherche_vers_mot (id, id_recherche)
            VALUES (%s, %s)
            RETURNING id
        ''', (id, id_recherche))
        bdd.cursor.fetchone()[0]
        bdd.conn.commit()

        return cls(id, mot)

    @classmethod
    def load(cls, id: int, bdd: "Bdd") -> Optional["MotCle"]:
        bdd.cursor.execute('SELECT mot FROM keywords WHERE id = %s', (id,))
        row = bdd.cursor.fetchone()
        if row:
            return cls(id, row[0])
        return None

    def supprimer(self, bdd: "Bdd") -> bool:
        try:
            # V�rifie si le mot-cl� est encore utilis�
            bdd.cursor.execute('SELECT COUNT(*) FROM recherche_vers_mot WHERE id_mot_cle = %s', (self.id,))
            count = bdd.cursor.fetchone()[0]
            if count > 0:
                print(f"Le mot-clé {self.id} est encore utilisé dans {count} recherche(s).")
                return False
            bdd.cursor.execute('DELETE FROM keywords WHERE id = %s', (self.id,))
            bdd.conn.commit()
            return True
        except Exception as e:
            print(f"Erreur lors de la suppression du mot-clé {self.id} : {e}")
            bdd.conn.rollback()
            return False

    def __str__(self) -> str:
        return f"MotCle(id={self.id}, mot='{self.mot}')"
