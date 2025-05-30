import sqlite3
from typing import List, Optional, Tuple
from datetime import datetime

class MotCle:
    def __init__(self, mot: str):
        self.mot = mot

class Image:
    def __init__(self, image):
        self.image = image

class Source:
    def __init__(self, url: str, description: str = ""):
        self.url = url
        self.description = description

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
    def __init__(self, id: int, id_espace: int, prompt: str, response: str, date_time: str, bdd: Bdd):
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
    def create(cls, id_espace: int, prompt: str, response: str, bdd: Bdd) -> 'Recherche':
        # Ajoute la recherche dans la base
        id_recherche = bdd.addRecherche(prompt, response)
        # Lie � l'espace
        bdd.addRechercheVersEspace(id_recherche, id_espace)
        # R�cup�re la date_time si besoin (ici, on suppose que addRecherche la renseigne)
        # � adapter selon ta m�thode
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return cls(id_recherche, id_espace, prompt, response, date_time, bdd)

    @classmethod
    def load(cls, id_recherche: int, bdd: "Bdd") -> "Recherche":
        # 1. R�cup�re les infos de la recherche
        bdd.cursor.execute('''
            SELECT id, prompt, response, date_time FROM recherches WHERE id = ?
        ''', (id_recherche,))
        row = bdd.cursor.fetchone()
        if row:
            id_rec, prompt, response, date_time = row
            # 2. R�cup�re l'id_espace depuis la table de jointure
            bdd.cursor.execute('''
                SELECT id_espace FROM recherche_espace WHERE id_recherche = ?
            ''', (id_recherche,))
            id_espace_row = bdd.cursor.fetchone()
            id_espace = id_espace_row[0] if id_espace_row else None
            # 3. Cr�e l'objet Recherche (attention � adapter le constructeur si besoin)
            return cls(
                id=id_rec,
                id_espace=id_espace,
                prompt=prompt,
                response=response,
                date_time=date_time,
                bdd=bdd
            )
        else:
            return None

    def __str__(self) -> str:
        return f"Recherche(id={self.id}, idEspace={self.id_espace}, prompt={self.prompt}, response={self.response}, date={self.date_time}"

    def ajouter_image(self, image) -> Image:
        img = Image(image)
        self.images.append(img)
        img_id = self.bdd.addImage(img)
        self.bdd.addRechercheVersImage(img_id, self.bdd.get_recherche_id(self))
        return img

    def ajouter_mot_cle(self, mot: str) -> MotCle:
        mot_cle = MotCle(mot)
        self.mots_cles.append(mot_cle)
        mot_cle_id = self.bdd.addKeyword(mot_cle)
        self.bdd.addRechercheVersMot(mot_cle_id, self.bdd.get_recherche_id(self))
        return mot_cle

    def ajouter_source(self, url: str, description: str = "") -> Source:
        source = Source(url, description)
        self.sources.append(source)
        source_id = self.bdd.addSource(source)
        self.bdd.addRechercheVersSource(source_id, self.bdd.get_recherche_id(self))
        return source

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



# Cr�er une instance de Bdd
bdd = Bdd("http://localhost:5444", "ndsds", "sd3qd32")

espaces = bdd.get_EspaceRecherche()

for espace in espaces:
    print(espace)
    recherches = espace.get_recherches()
    for recherche in recherches:
        print(recherche)


bdd.close()
