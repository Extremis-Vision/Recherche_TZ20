from typing import Optional
from datetime import datetime
from .Image import Image
from .Source import Source
from .MotCle import MotCle

class Recherche:
    def __init__(self, id: int, id_espace: int, prompt: str, response: str, date_time: str, bdd: "Bdd"):
        self.id = id
        self.id_espace = id_espace
        self.prompt = prompt
        self.response = response
        self.date_time = date_time
        self.bdd = bdd
        self.images = []
        self.mots_cles = []
        self.sources = []

    @classmethod
    def create(cls, id_espace: int, prompt: str, response: str, bdd: "Bdd") -> "Recherche":
        # Ajoute la recherche dans la base
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        bdd.cursor.execute('''
            INSERT INTO recherches (prompt, response, date_time)
            VALUES (%s, %s, %s)
            RETURNING id
        ''', (prompt, response, now))
        id_recherche = bdd.cursor.fetchone()[0]
        # Lie � l'espace
        bdd.cursor.execute('''
            INSERT INTO recherche_espace (id_recherche, id_espace)
            VALUES (%s, %s)
        ''', (id_recherche, id_espace))
        bdd.conn.commit()
        return cls(id_recherche, id_espace, prompt, response, now, bdd)

    @classmethod
    def load(cls, id_recherche: int, bdd: "Bdd") -> Optional["Recherche"]:
        bdd.cursor.execute('''
            SELECT id, prompt, response, date_time FROM recherches WHERE id = %s
        ''', (id_recherche,))
        row = bdd.cursor.fetchone()
        if row:
            id_rec, prompt, response, date_time = row
            bdd.cursor.execute('''
                SELECT id_espace FROM recherche_espace WHERE id_recherche = %s
            ''', (id_recherche,))
            id_espace_row = bdd.cursor.fetchone()
            id_espace = id_espace_row[0] if id_espace_row else None
            recherche = cls(id_rec, id_espace, prompt, response, date_time, bdd)
            # Charge les images, mots-cl�s, sources associ�s
            # (Optionnel, tu peux le faire � la demande avec des m�thodes sp�cifiques)
            return recherche
        return None

    def __str__(self) -> str:
        return f"Recherche(id={self.id}, idEspace={self.id_espace}, prompt={self.prompt}, response={self.response}, date={self.date_time})"

    def ajouter_image(self, image_data) -> "Image":
        image = Image.create(image_data, self.bdd)
        self.images.append(image)
        self.bdd.cursor.execute('''
            INSERT INTO recherche_vers_image (id_image, id_recherche)
            VALUES (%s, %s)
        ''', (image.id, self.id))
        self.bdd.conn.commit()
        return image

    def ajouter_mot_cle(self, mot: str) -> "MotCle":
        mot_cle = MotCle.create(mot, self.bdd)
        self.mots_cles.append(mot_cle)
        self.bdd.cursor.execute('''
            INSERT INTO recherche_vers_mot (id_mot_cle, id_recherche)
            VALUES (%s, %s)
        ''', (mot_cle.id, self.id))
        self.bdd.conn.commit()
        return mot_cle

    def ajouter_source(self, url: str, description: str = "") -> "Source":
        source = Source.create(url, description, self.bdd)
        self.sources.append(source)
        self.bdd.cursor.execute('''
            INSERT INTO recherche_vers_source (id_source, id_recherche)
            VALUES (%s, %s)
        ''', (source.id, self.id))
        self.bdd.conn.commit()
        return source

    def supprimer(self) -> bool:
        try:
            # 1. R�cup�re les objets associ�s � la recherche
            self.bdd.cursor.execute('''
                SELECT id_image FROM recherche_vers_image WHERE id_recherche = %s
            ''', (self.id,))
            image_ids = [row[0] for row in self.bdd.cursor.fetchall()]
            self.bdd.cursor.execute('''
                SELECT id_mot_cle FROM recherche_vers_mot WHERE id_recherche = %s
            ''', (self.id,))
            mot_cle_ids = [row[0] for row in self.bdd.cursor.fetchall()]
            self.bdd.cursor.execute('''
                SELECT id_source FROM recherche_vers_source WHERE id_recherche = %s
            ''', (self.id,))
            source_ids = [row[0] for row in self.bdd.cursor.fetchall()]

            # 2. Supprime les liens de la recherche
            self.bdd.cursor.execute('''
                DELETE FROM recherche_vers_image WHERE id_recherche = %s
            ''', (self.id,))
            self.bdd.cursor.execute('''
                DELETE FROM recherche_vers_mot WHERE id_recherche = %s
            ''', (self.id,))
            self.bdd.cursor.execute('''
                DELETE FROM recherche_vers_source WHERE id_recherche = %s
            ''', (self.id,))
            self.bdd.cursor.execute('''
                DELETE FROM recherche_espace WHERE id_recherche = %s
            ''', (self.id,))

            # 3. Supprime la recherche elle-m�me
            self.bdd.cursor.execute('''
                DELETE FROM recherches WHERE id = %s
            ''', (self.id,))

            # 4. Pour chaque image/mot-cl�/source, v�rifie s'il est encore utilis� ailleurs
            # Si non, supprime-le (avec la m�thode supprimer de la classe)
            for image_id in image_ids:
                image = Image.load(image_id, self.bdd)
                if image:
                    image.supprimer(self.bdd)  # La m�thode supprimer v�rifie l'utilisation

            for mot_cle_id in mot_cle_ids:
                mot_cle = MotCle.load(mot_cle_id, self.bdd)
                if mot_cle:
                    mot_cle.supprimer(self.bdd)

            for source_id in source_ids:
                source = Source.load(source_id, self.bdd)
                if source:
                    source.supprimer(self.bdd)

            self.bdd.conn.commit()
            return True
        except Exception as e:
            print(f"Erreur lors de la suppression de la recherche {self.id} : {e}")
            self.bdd.conn.rollback()
            return False
