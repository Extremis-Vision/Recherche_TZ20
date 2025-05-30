from typing import Optional

class Source:
    def __init__(self, id: int, url: str, description: str = ""):
        self.id = id
        self.url = url
        self.description = description

    @classmethod
    def create(cls, url: str, description: str, bdd: "Bdd") -> "Source":
        bdd.cursor.execute('''
            INSERT INTO sources (url, description)
            VALUES (%s, %s)
            RETURNING id
        ''', (url, description))
        id = bdd.cursor.fetchone()[0]
        bdd.conn.commit()
        return cls(id, url, description)

    @classmethod
    def load(cls, id: int, bdd: "Bdd") -> Optional["Source"]:
        bdd.cursor.execute('SELECT url, description FROM sources WHERE id = %s', (id,))
        row = bdd.cursor.fetchone()
        if row:
            return cls(id, row[0], row[1])
        return None

    def supprimer(self, bdd: "Bdd") -> bool:
        try:
            # V�rifie si la source est encore utilis�e
            bdd.cursor.execute('SELECT COUNT(*) FROM recherche_vers_source WHERE id_source = %s', (self.id,))
            count = bdd.cursor.fetchone()[0]
            if count > 0:
                print(f"La source {self.id} est encore utilis�e dans {count} recherche(s).")
                return False
            bdd.cursor.execute('DELETE FROM sources WHERE id = %s', (self.id,))
            bdd.conn.commit()
            return True
        except Exception as e:
            print(f"Erreur lors de la suppression de la source {self.id} : {e}")
            bdd.conn.rollback()
            return False

    def __str__(self) -> str:
        return f"Source(id={self.id}, url='{self.url}', description='{self.description}')"

