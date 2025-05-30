import psycopg2
from typing import List, Optional, Tuple
from datetime import datetime
from dotenv import load_dotenv
import os

chemin_env = os.path.join(os.path.dirname(__file__), '..', '.env')

load_dotenv(chemin_env)

class MotCle:
    def __init__(self, id: int, mot: str):
        self.id = id
        self.mot = mot

    @classmethod
    def create(cls, mot: str, bdd: "Bdd") -> "MotCle":
        bdd.cursor.execute('''
            INSERT INTO keywords (mot)
            VALUES (%s)
            RETURNING id
        ''', (mot,))
        id = bdd.cursor.fetchone()[0]
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
                print(f"Le mot-cl� {self.id} est encore utilis� dans {count} recherche(s).")
                return False
            bdd.cursor.execute('DELETE FROM keywords WHERE id = %s', (self.id,))
            bdd.conn.commit()
            return True
        except Exception as e:
            print(f"Erreur lors de la suppression du mot-cl� {self.id} : {e}")
            bdd.conn.rollback()
            return False

    def __str__(self) -> str:
        return f"MotCle(id={self.id}, mot='{self.mot}')"

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

class Bdd:
    def __init__(self):
        self.conn = psycopg2.connect(
            host=os.getenv('POSTGRES_HOST'),
            port=os.getenv('POSTGRES_PORT'),
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD'),
            database=os.getenv('POSTGRES_DB')
        )
        self.cursor = self.conn.cursor()
        self._init_db()

    def _init_db(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS keywords (
                id SERIAL PRIMARY KEY,
                mot TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS prompts (
                id SERIAL PRIMARY KEY,
                prompt TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS question_engines (
                id SERIAL PRIMARY KEY,
                question TEXT,
                engines TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS images (
                id SERIAL PRIMARY KEY,
                image BYTEA
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS recherches (
                id SERIAL PRIMARY KEY,
                prompt TEXT,
                response TEXT,
                date_time TIMESTAMP
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS recherche_espaces (
                id SERIAL PRIMARY KEY,
                subject TEXT,
                date_time TIMESTAMP,
                objectif TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS sources (
                id SERIAL PRIMARY KEY,
                url TEXT,
                description TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS recherche_vers_mot (
                id SERIAL PRIMARY KEY,
                id_mot_cle INTEGER REFERENCES keywords(id),
                id_recherche INTEGER REFERENCES recherches(id)
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS recherche_vers_image (
                id SERIAL PRIMARY KEY,
                id_image INTEGER REFERENCES images(id),
                id_recherche INTEGER REFERENCES recherches(id)
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS recherche_vers_source (
                id SERIAL PRIMARY KEY,
                id_source INTEGER REFERENCES sources(id),
                id_recherche INTEGER REFERENCES recherches(id)
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS recherche_espace (
                id SERIAL PRIMARY KEY,
                id_recherche INTEGER REFERENCES recherches(id),
                id_espace INTEGER REFERENCES recherche_espaces(id)
            )
        ''')
        self.conn.commit()


    def addKeyword(self, mot_cle: 'MotCle') -> int:
        self.cursor.execute('''
            INSERT INTO keywords (mot)
            VALUES (%s)
            RETURNING id
        ''', (mot_cle.mot,))
        self.conn.commit()
        return self.cursor.fetchone()[0]

    def addPrompt(self, prompt: str) -> int:
        self.cursor.execute('''
            INSERT INTO prompts (prompt)
            VALUES (%s)
            RETURNING id
        ''', (prompt,))
        self.conn.commit()
        return self.cursor.fetchone()[0]

    def addQuestionEngines(self, question: str, engines: List[str]) -> int:
        engines_str = ','.join(engines)
        self.cursor.execute('''
            INSERT INTO question_engines (question, engines)
            VALUES (%s, %s)
            RETURNING id
        ''', (question, engines_str))
        self.conn.commit()
        return self.cursor.fetchone()[0]

    def addImage(self, image: 'Image') -> int:
        self.cursor.execute('''
            INSERT INTO images (image)
            VALUES (%s)
            RETURNING id
        ''', (image.image,))
        self.conn.commit()
        return self.cursor.fetchone()[0]

    def addRecherche(self, recherche: 'Recherche') -> int:
        self.cursor.execute('''
            INSERT INTO recherches (prompt, response, date_time)
            VALUES (%s, %s, %s)
            RETURNING id
        ''', (recherche.prompt, recherche.response, recherche.date_time))
        self.conn.commit()
        return self.cursor.fetchone()[0]

    def addRechercheEspace(self, espace_recherche: 'RechercheEspace') -> int:
        self.cursor.execute('''
            INSERT INTO recherche_espaces (subject, date_time, objectif)
            VALUES (%s, %s, %s)
            RETURNING id
        ''', (espace_recherche.subject, espace_recherche.date_time, espace_recherche.objectif))
        self.conn.commit()
        return self.cursor.fetchone()[0]

    def addSource(self, source: 'Source') -> int:
        self.cursor.execute('''
            INSERT INTO sources (url, description)
            VALUES (%s, %s)
            RETURNING id
        ''', (source.url, source.description))
        self.conn.commit()
        return self.cursor.fetchone()[0]

    def addRechercheVersMot(self, id_mot_cle: int, id_recherche: int):
        self.cursor.execute('''
            INSERT INTO recherche_vers_mot (id_mot_cle, id_recherche)
            VALUES (%s, %s)
        ''', (id_mot_cle, id_recherche))
        self.conn.commit()

    def addRechercheVersImage(self, id_image: int, id_recherche: int):
        self.cursor.execute('''
            INSERT INTO recherche_vers_image (id_image, id_recherche)
            VALUES (%s, %s)
        ''', (id_image, id_recherche))
        self.conn.commit()

    def addRechercheVersSource(self, id_source: int, id_recherche: int):
        self.cursor.execute('''
            INSERT INTO recherche_vers_source (id_source, id_recherche)
            VALUES (%s, %s)
        ''', (id_source, id_recherche))
        self.conn.commit()

    def addRechercheEspaceVersRecherche(self, id_recherche: int, id_espace: int):
        self.cursor.execute('''
            INSERT INTO recherche_espace (id_recherche, id_espace)
            VALUES (%s, %s)
        ''', (id_recherche, id_espace))
        self.conn.commit()

    def get_EspaceRecherche(self) -> List["RechercheEspace"]:
        self.cursor.execute('''
            SELECT id FROM recherche_espaces
        ''')
        espaces = []
        for (id_espace,) in self.cursor.fetchall():
            espace = RechercheEspace.load(id_espace, self)
            if espace:
                espaces.append(espace)
        return espaces

    def close(self):
        self.conn.close()

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

class RechercheEspace:
    def __init__(self, id: int, subject: str, objectif: str, date_time: str, bdd: "Bdd"):
        self.id = id
        self.subject = subject
        self.objectif = objectif
        self.date_time = date_time
        self.bdd = bdd

    @classmethod
    def create(cls, subject: str, objectif: str, bdd: "Bdd") -> "RechercheEspace":
        # Ajoute l'espace dans la base (supposons que addRechercheEspace renvoie l'id)
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

if __name__ == "__main__":
    bdd = Bdd()
    try:
        # Cr�e un mot-cl�
        mot_cle = MotCle.create("test_postgresql", bdd)
        print("Mot-cl� cr�� :", mot_cle)

        # Charge le mot-cl�
        mot_cle_charge = MotCle.load(mot_cle.id, bdd)
        print("Mot-cl� charg� :", mot_cle_charge)
    finally:
        bdd.close()
