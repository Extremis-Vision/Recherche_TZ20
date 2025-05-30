import sqlite3
from typing import List, Optional, Tuple
from datetime import datetime

class MotCle:
    def __init__(self, id: int, mot: str):
        self.id = id
        self.mot = mot

    @classmethod
    def create(cls, mot: str, bdd: "Bdd") -> "MotCle":
        bdd.cursor.execute('INSERT INTO keywords (mot) VALUES (?)', (mot,))
        id = bdd.cursor.lastrowid
        bdd.conn.commit()
        return cls(id, mot)

    @classmethod
    def load(cls, id: int, bdd: "Bdd") -> Optional["MotCle"]:
        bdd.cursor.execute('SELECT mot FROM keywords WHERE id = ?', (id,))
        row = bdd.cursor.fetchone()
        if row:
            return cls(id, row[0])
        return None

    def supprimer(self, bdd: "Bdd") -> bool:
        try:
            # V�rifie si le mot-cl� est encore utilis�
            bdd.cursor.execute('SELECT COUNT(*) FROM recherche_vers_mot WHERE id_mot_cle = ?', (self.id,))
            count = bdd.cursor.fetchone()[0]
            if count > 0:
                print(f"Le mot-cl� {self.id} est encore utilis� dans {count} recherche(s).")
                return False
            bdd.cursor.execute('DELETE FROM keywords WHERE id = ?', (self.id,))
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
        bdd.cursor.execute('INSERT INTO images (image) VALUES (?)', (image_data,))
        id = bdd.cursor.lastrowid
        bdd.conn.commit()
        return cls(id, image_data)

    @classmethod
    def load(cls, id: int, bdd: "Bdd") -> Optional["Image"]:
        bdd.cursor.execute('SELECT image FROM images WHERE id = ?', (id,))
        row = bdd.cursor.fetchone()
        if row:
            return cls(id, row[0])
        return None

    def supprimer(self, bdd: "Bdd") -> bool:
        try:
            # V�rifie si l'image est encore utilis�e
            bdd.cursor.execute('SELECT COUNT(*) FROM recherche_vers_image WHERE id_image = ?', (self.id,))
            count = bdd.cursor.fetchone()[0]
            if count > 0:
                print(f"L'image {self.id} est encore utilis�e dans {count} recherche(s).")
                return False
            bdd.cursor.execute('DELETE FROM images WHERE id = ?', (self.id,))
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
        bdd.cursor.execute('INSERT INTO sources (url, description) VALUES (?, ?)', (url, description))
        id = bdd.cursor.lastrowid
        bdd.conn.commit()
        return cls(id, url, description)

    @classmethod
    def load(cls, id: int, bdd: "Bdd") -> Optional["Source"]:
        bdd.cursor.execute('SELECT url, description FROM sources WHERE id = ?', (id,))
        row = bdd.cursor.fetchone()
        if row:
            return cls(id, row[0], row[1])
        return None

    def supprimer(self, bdd: "Bdd") -> bool:
        try:
            # V�rifie si la source est encore utilis�e
            bdd.cursor.execute('SELECT COUNT(*) FROM recherche_vers_source WHERE id_source = ?', (self.id,))
            count = bdd.cursor.fetchone()[0]
            if count > 0:
                print(f"La source {self.id} est encore utilis�e dans {count} recherche(s).")
                return False
            bdd.cursor.execute('DELETE FROM sources WHERE id = ?', (self.id,))
            bdd.conn.commit()
            return True
        except Exception as e:
            print(f"Erreur lors de la suppression de la source {self.id} : {e}")
            bdd.conn.rollback()
            return False

    def __str__(self) -> str:
        return f"Source(id={self.id}, url='{self.url}', description='{self.description}')"


class Bdd:
    def __init__(self, url: str, username: str, mdp: str):
        self.url = url
        self.username = username
        self.mdp = mdp
        self.conn = sqlite3.connect('bdd.db')
        self.cursor = self.conn.cursor()
        self._init_db()

    def _init_db(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS keywords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mot TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS prompts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                prompt TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS question_engines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT,
                engines TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS images (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                image BLOB
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS recherches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                prompt TEXT,
                response TEXT,
                date_time DATETIME
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS recherche_espaces (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject TEXT,
                date_time DATETIME,
                objectif TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS sources (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT,
                description TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS recherche_vers_mot (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_mot_cle INTEGER,
                id_recherche INTEGER,
                FOREIGN KEY (id_mot_cle) REFERENCES keywords(id),
                FOREIGN KEY (id_recherche) REFERENCES recherches(id)
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS recherche_vers_image (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_image INTEGER,
                id_recherche INTEGER,
                FOREIGN KEY (id_image) REFERENCES images(id),
                FOREIGN KEY (id_recherche) REFERENCES recherches(id)
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS recherche_vers_source (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_source INTEGER,
                id_recherche INTEGER,
                FOREIGN KEY (id_source) REFERENCES sources(id),
                FOREIGN KEY (id_recherche) REFERENCES recherches(id)
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS recherche_espace (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_recherche INTEGER,
                id_espace INTEGER,
                FOREIGN KEY (id_recherche) REFERENCES recherches(id),
                FOREIGN KEY (id_espace) REFERENCES recherche_espaces(id)
            )
        ''')
        self.conn.commit()

    def addKeyword(self, mot_cle: 'MotCle') -> int:
        self.cursor.execute('''
            INSERT INTO keywords (mot)
            VALUES (?)
        ''', (mot_cle.mot,))
        self.conn.commit()
        return self.cursor.lastrowid

    def addPrompt(self, prompt: str) -> int:
        self.cursor.execute('''
            INSERT INTO prompts (prompt)
            VALUES (?)
        ''', (prompt,))
        self.conn.commit()
        return self.cursor.lastrowid

    def addQuestionEngines(self, question: str, engines: List[str]) -> int:
        engines_str = ','.join(engines)
        self.cursor.execute('''
            INSERT INTO question_engines (question, engines)
            VALUES (?, ?)
        ''', (question, engines_str))
        self.conn.commit()
        return self.cursor.lastrowid

    def addImage(self, image: 'Image') -> int:
        self.cursor.execute('''
            INSERT INTO images (image)
            VALUES (?)
        ''', (image.image,))
        self.conn.commit()
        return self.cursor.lastrowid

    def addRecherche(self, recherche: 'Recherche') -> int:
        self.cursor.execute('''
            INSERT INTO recherches (prompt, response, date_time)
            VALUES (?, ?, ?)
        ''', (recherche.prompt, recherche.response, recherche.date_time))
        self.conn.commit()
        return self.cursor.lastrowid

    def addRechercheEspace(self, espace_recherche: 'RechercheEspace') -> int:
        self.cursor.execute('''
            INSERT INTO recherche_espaces (subject, date_time, objectif)
            VALUES (?, ?, ?)
        ''', (espace_recherche.subject, espace_recherche.date_time, espace_recherche.objectif))
        self.conn.commit()
        return self.cursor.lastrowid

    def addSource(self, source: 'Source') -> int:
        self.cursor.execute('''
            INSERT INTO sources (url, description)
            VALUES (?, ?)
        ''', (source.url, source.description))
        self.conn.commit()
        return self.cursor.lastrowid

    def addRechercheVersMot(self, id_mot_cle: int, id_recherche: int):
        self.cursor.execute('''
            INSERT INTO recherche_vers_mot (id_mot_cle, id_recherche)
            VALUES (?, ?)
        ''', (id_mot_cle, id_recherche))
        self.conn.commit()

    def addRechercheVersImage(self, id_image: int, id_recherche: int):
        self.cursor.execute('''
            INSERT INTO recherche_vers_image (id_image, id_recherche)
            VALUES (?, ?)
        ''', (id_image, id_recherche))
        self.conn.commit()

    def addRechercheVersSource(self, id_source: int, id_recherche: int):
        self.cursor.execute('''
            INSERT INTO recherche_vers_source (id_source, id_recherche)
            VALUES (?, ?)
        ''', (id_source, id_recherche))
        self.conn.commit()

    def addRechercheEspaceVersRecherche(self, id_recherche: int, id_espace: int):
        self.cursor.execute('''
            INSERT INTO recherche_espace (id_recherche, id_espace)
            VALUES (?, ?)
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
        bdd.cursor.execute('INSERT INTO recherches (prompt, response, date_time) VALUES (?, ?, ?)',
                          (prompt, response, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        id_recherche = bdd.cursor.lastrowid
        # Lie � l'espace
        bdd.cursor.execute('INSERT INTO recherche_espace (id_recherche, id_espace) VALUES (?, ?)',
                          (id_recherche, id_espace))
        bdd.conn.commit()
        return cls(id_recherche, id_espace, prompt, response, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), bdd)

    @classmethod
    def load(cls, id_recherche: int, bdd: "Bdd") -> Optional["Recherche"]:
        bdd.cursor.execute('SELECT id, prompt, response, date_time FROM recherches WHERE id = ?', (id_recherche,))
        row = bdd.cursor.fetchone()
        if row:
            id_rec, prompt, response, date_time = row
            bdd.cursor.execute('SELECT id_espace FROM recherche_espace WHERE id_recherche = ?', (id_recherche,))
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
        self.bdd.cursor.execute('INSERT INTO recherche_vers_image (id_image, id_recherche) VALUES (?, ?)',
                              (image.id, self.id))
        self.bdd.conn.commit()
        return image

    def ajouter_mot_cle(self, mot: str) -> "MotCle":
        mot_cle = MotCle.create(mot, self.bdd)
        self.mots_cles.append(mot_cle)
        self.bdd.cursor.execute('INSERT INTO recherche_vers_mot (id_mot_cle, id_recherche) VALUES (?, ?)',
                              (mot_cle.id, self.id))
        self.bdd.conn.commit()
        return mot_cle

    def ajouter_source(self, url: str, description: str = "") -> "Source":
        source = Source.create(url, description, self.bdd)
        self.sources.append(source)
        self.bdd.cursor.execute('INSERT INTO recherche_vers_source (id_source, id_recherche) VALUES (?, ?)',
                              (source.id, self.id))
        self.bdd.conn.commit()
        return source

    def supprimer(self) -> bool:
        try:
            # 1. R�cup�re les objets associ�s � la recherche
            self.bdd.cursor.execute('SELECT id_image FROM recherche_vers_image WHERE id_recherche = ?', (self.id,))
            image_ids = [row[0] for row in self.bdd.cursor.fetchall()]
            self.bdd.cursor.execute('SELECT id_mot_cle FROM recherche_vers_mot WHERE id_recherche = ?', (self.id,))
            mot_cle_ids = [row[0] for row in self.bdd.cursor.fetchall()]
            self.bdd.cursor.execute('SELECT id_source FROM recherche_vers_source WHERE id_recherche = ?', (self.id,))
            source_ids = [row[0] for row in self.bdd.cursor.fetchall()]

            # 2. Supprime les liens de la recherche
            self.bdd.cursor.execute('DELETE FROM recherche_vers_image WHERE id_recherche = ?', (self.id,))
            self.bdd.cursor.execute('DELETE FROM recherche_vers_mot WHERE id_recherche = ?', (self.id,))
            self.bdd.cursor.execute('DELETE FROM recherche_vers_source WHERE id_recherche = ?', (self.id,))
            self.bdd.cursor.execute('DELETE FROM recherche_espace WHERE id_recherche = ?', (self.id,))

            # 3. Supprime la recherche elle-m�me
            self.bdd.cursor.execute('DELETE FROM recherches WHERE id = ?', (self.id,))

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
    def __init__(self, id: int, subject: str, objectif: str, date_time: str, bdd: Bdd):
        self.id = id
        self.subject = subject
        self.objectif = objectif
        self.date_time = date_time
        self.bdd = bdd

    
    @classmethod
    def create(cls, subject: str, objectif: str, bdd: Bdd) -> 'RechercheEspace':
        # Ajoute l'espace dans la base
        id_espace = bdd.addRechercheEspace(subject, objectif)
        # R�cup�re la date_time si besoin
        # (� adapter selon ta m�thode addRechercheEspace)
        # Ici, on suppose que addRechercheEspace renvoie l'id
        return cls(id_espace, subject, objectif, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), bdd)

    @classmethod
    def load(cls, id_espace: int, bdd: Bdd) -> 'RechercheEspace':
        # Charge l'espace depuis la base
        bdd.cursor.execute('''
            SELECT subject, date_time, objectif FROM recherche_espaces WHERE id = ?
        ''', (id_espace,))
        row = bdd.cursor.fetchone()
        if row:
            subject, date_time, objectif = row
            return cls(id_espace, subject, objectif, date_time, bdd)
        else:
            return None

    def __str__(self) -> str:
        return f"RechercheEspace(id={self.id}, subject='{self.subject}', objectif='{self.objectif}', date_time='{self.date_time}')"

    def create_recherche(self, prompt: str, response: str) -> 'Recherche':
        recherche = Recherche(self.id, prompt, response, self.bdd)
        recherche_id = self.bdd.addRecherche(recherche)
        self.bdd.addRechercheEspaceVersRecherche(recherche_id, self.id)
        return recherche

    def get_recherches(self) -> List["Recherche"]:
        # R�cup�re les IDs des recherches associ�es � cet espace
        self.bdd.cursor.execute('''
            SELECT id_recherche FROM recherche_espace WHERE id_espace = ?
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
            self.bdd.cursor.execute('DELETE FROM recherche_espaces WHERE id = ?', (self.id,))
            self.bdd.conn.commit()
            return True
        except Exception as e:
            print(f"Erreur lors de la suppression de l'espace {self.id} : {e}")
            self.bdd.conn.rollback()
            return False



# Cr�er une instance de Bdd
bdd = Bdd("http://localhost:5444", "ndsds", "sd3qd32")

espaces = bdd.get_EspaceRecherche()

for espace in espaces:
    print(espace)
    recherches = espace.get_recherches()
    for recherche in recherches:
        print(recherche)

espaces[1].supprimer()

espaces = bdd.get_EspaceRecherche()
for espace in espaces:
    print(espace)
    recherches = espace.get_recherches()
    for recherche in recherches:
        print(recherche)

espaces[0].supprimer()

bdd.close()
