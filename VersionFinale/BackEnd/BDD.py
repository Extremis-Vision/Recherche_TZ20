import sqlite3
from typing import List, Optional
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

    def addRechercheEspace(self, id_recherche: int, id_espace: int):
        self.cursor.execute('''
            INSERT INTO recherche_espace (id_recherche, id_espace)
            VALUES (?, ?)
        ''', (id_recherche, id_espace))
        self.conn.commit()

    def get_recherche_id(self, recherche: 'Recherche') -> Optional[int]:
        self.cursor.execute('''
            SELECT id FROM recherches WHERE prompt = ? AND response = ? AND date_time = ?
        ''', (recherche.prompt, recherche.response, recherche.date_time))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def close(self):
        self.conn.close()

class Recherche:
    def __init__(self, id_espace: int, prompt: str, response: str, bdd: Bdd):
        self.id_espace = id_espace
        self.prompt = prompt
        self.response = response
        self.date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.bdd = bdd
        self.images = []
        self.mots_cles = []
        self.sources = []

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
    def __init__(self, subject: str, objectif: str = "", bdd: Bdd = None):
        self.subject = subject
        self.date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.objectif = objectif
        self.bdd = bdd
        self.id = None

    def create_recherche(self, prompt: str, response: str) -> 'Recherche':
        recherche = Recherche(self.id, prompt, response, self.bdd)
        recherche_id = self.bdd.addRecherche(recherche)
        self.bdd.addRechercheEspace(recherche_id, self.id)
        return recherche

    def get_recherche(self, recherche_id: int) -> 'Recherche':
        # R�cup�rer une recherche existante � partir de la base de donn�es
        self.bdd.cursor.execute('''
            SELECT prompt, response, date_time FROM recherches WHERE id = ?
        ''', (recherche_id,))
        result = self.bdd.cursor.fetchone()
        if result:
            prompt, response, date_time = result
            return Recherche(self.id, prompt, response, self.bdd)
        else:
            return None



# Cr�er une instance de Bdd
bdd = Bdd("http://localhost:5444", "ndsds", "sd3qd32")

# Cr�er un nouvel espace de recherche
espace_recherche = RechercheEspace("test", "faire en sorte de tester le projet", bdd)
espace_recherche.id = bdd.addRechercheEspace(espace_recherche)

# Cr�er une nouvelle recherche li�e � l'espace de recherche
recherche = espace_recherche.create_recherche("Qu'est ce qu'un test", "R�ponse de recherche")

# Ajouter une image � la recherche
image = recherche.ajouter_image("exemple_image")

# Ajouter un mot-cl� � la recherche
mot_cle = recherche.ajouter_mot_cle("exemple")

# Ajouter une source � la recherche
source = recherche.ajouter_source("http://exemple.com", "description_exemple")

# R�cup�rer une recherche existante
recherche_existante = espace_recherche.get_recherche(recherche_id=1)
if recherche_existante:
    print("Recherche existante trouv�e:", recherche_existante.prompt)

# Fermer la connexion � la base de donn�es
bdd.close()
