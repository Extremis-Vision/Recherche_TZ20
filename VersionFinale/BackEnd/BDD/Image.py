from typing import Optional

class Image:
    def __init__(self, id: int, image_data):
        self.id = id
        self.image_data = image_data

    @classmethod
    def create(cls, image_data, bdd: "Bdd") -> "Image":
        bdd.cursor.execute('''
            INSERT INTO images (image)
            VALUES (%s)
            RETURNING id
        ''', (image_data,))
        id = bdd.cursor.fetchone()[0]
        bdd.conn.commit()
        return cls(id, image_data)

    @classmethod
    def load(cls, id: int, bdd: "Bdd") -> Optional["Image"]:
        bdd.cursor.execute('SELECT image FROM images WHERE id = %s', (id,))
        row = bdd.cursor.fetchone()
        if row:
            return cls(id, row[0])
        return None

    def supprimer(self, bdd: "Bdd") -> bool:
        try:
            # V�rifie si l'image est encore utilis�e
            bdd.cursor.execute('SELECT COUNT(*) FROM recherche_vers_image WHERE id_image = %s', (self.id,))
            count = bdd.cursor.fetchone()[0]
            if count > 0:
                print(f"L'image {self.id} est encore utilis�e dans {count} recherche(s).")
                return False
            bdd.cursor.execute('DELETE FROM images WHERE id = %s', (self.id,))
            bdd.conn.commit()
            return True
        except Exception as e:
            print(f"Erreur lors de la suppression de l'image {self.id} : {e}")
            bdd.conn.rollback()
            return False

    def __str__(self) -> str:
        return f"Image(id={self.id}, image_data='{self.image_data[:20]}...')"  # Affichage raccourci pour l'exemple
