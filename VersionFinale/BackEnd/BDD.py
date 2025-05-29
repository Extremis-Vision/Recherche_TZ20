import sqlite3
from typing import List
from datetime import datetime

class MotCle: 
    def __init__(self, mot : str):
        self.mot = mot


class Image: 
    def __init__(self, image):
        self.image = image

class Recherche:
    def __init__(self, prompt: str, response: str):
        self.prompt = prompt
        self.response = response
        self.date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class RechercheEspace:
    def __init__(self, subject: str, objectif: str = ""):
        self.subject = subject
        self.date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.objectif = objectif

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
        # Initialiser la base de donn�es
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
                FOREIGN KEY (id_mot_cle) REFERENCES keywords(id),
                FOREIGN KEY (id_recherche) REFERENCES recherches(id)
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS recherche_vers_image (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                FOREIGN KEY (id_image) REFERENCES images(id),
                FOREIGN KEY (id_recherche) REFERENCES recherches(id)
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS recherche_vers_source (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                FOREIGN KEY (id_source) REFERENCES sources(id),
                FOREIGN KEY (id_recherche) REFERENCES recherches(id)
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS recherche_espace (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                FOREIGN KEY (id_recherche) REFERENCES recherches(id),
                FOREIGN KEY (id_espace) REFERENCES recherche_espaces(id)
            )
        ''')
        self.conn.commit()

    def addKeyword(self, mot: str):
        # Ajouter un mot-cl� � la base de donn�es
        self.cursor.execute('''
            INSERT INTO keywords (mot)
            VALUES (?)
        ''', (mot,))
        self.conn.commit()
        return self.cursor.lastrowid

    def addPrompt(self, prompt: str):
        # Ajouter un prompt � la base de donn�es
        self.cursor.execute('''
            INSERT INTO prompts (prompt)
            VALUES (?)
        ''', (prompt,))
        self.conn.commit()

    def addQuestionEngines(self, question: str, engines: List[str]):
        # Ajouter une question et les moteurs de recherche associ�s � la base de donn�es
        engines_str = ','.join(engines)
        self.cursor.execute('''
            INSERT INTO question_engines (question, engines)
            VALUES (?, ?)
        ''', (question, engines_str))
        self.conn.commit()

    def addImage(self, image):
        # Ajouter une image � la base de donn�es
        self.cursor.execute('''
            INSERT INTO images (image)
            VALUES (?)
        ''', (image,))
        self.conn.commit()
        return self.cursor.lastrowid

    def addRecherche(self, prompt: str, response: str, timestamp: str):
        # Ajouter une recherche � la base de donn�es
        self.cursor.execute('''
            INSERT INTO recherches (prompt, response, timestamp)
            VALUES (?, ?, ?)
        ''', (prompt, response, timestamp))
        self.conn.commit()
        return self.cursor.lastrowid

    def addRechercheEspace(self, subject: str, date_time: str, objectif: str):
        # Ajouter une recherche espace � la base de donn�es
        self.cursor.execute('''
            INSERT INTO recherche_espaces (subject, date_time, objectif)
            VALUES (?, ?, ?)
        ''', (subject, date_time, objectif))
        self.conn.commit()
        return self.cursor.lastrowid

    def addSource(self, url: str, description: str):
        # Ajouter une source � la base de donn�es
        self.cursor.execute('''
            INSERT INTO sources (url, description)
            VALUES (?, ?)
        ''', (url, description))
        self.conn.commit()
        return self.cursor.lastrowid

    def addRechercheVersMot(self, id_mot_cle: int, id_recherche: int):
        # Ajouter une association entre une recherche et un mot-cl�
        self.cursor.execute('''
            INSERT INTO recherche_vers_mot (id_mot_cle, id_recherche)
            VALUES (?, ?)
        ''', (id_mot_cle, id_recherche))
        self.conn.commit()

    def addRechercheVersImage(self, id_image: int, id_recherche: int):
        # Ajouter une association entre une recherche et une image
        self.cursor.execute('''
            INSERT INTO recherche_vers_image (id_image, id_recherche)
            VALUES (?, ?)
        ''', (id_image, id_recherche))
        self.conn.commit()

    def addRechercheVersSource(self, id_source: int, id_recherche: int):
        # Ajouter une association entre une recherche et une source
        self.cursor.execute('''
            INSERT INTO recherche_vers_source (id_source, id_recherche)
            VALUES (?, ?)
        ''', (id_source, id_recherche))
        self.conn.commit()

    def addRechercheEspace(self, id_recherche: int, id_espace: int):
        # Ajouter une association entre une recherche et un espace
        self.cursor.execute('''
            INSERT INTO recherche_espace (id_recherche, id_espace)
            VALUES (?, ?)
        ''', (id_recherche, id_espace))
        self.conn.commit()

    def close(self):
        # Fermer la connexion � la base de donn�es
        self.conn.close()

bdd = Bdd("http://localhost:5444", "ndsds", "sd3qd32")
