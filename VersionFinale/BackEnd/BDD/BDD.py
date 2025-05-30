import psycopg2
from typing import List
from dotenv import load_dotenv
import os
from .Image import Image
from .Source import Source
from .MotCle import MotCle
from .Recherche import Recherche
from .RechercheEspace import RechercheEspace


chemin_env = os.path.join(os.path.dirname(__file__), '..', '..', '.env')

load_dotenv(chemin_env)

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
    
    def get_MotCle(self) -> List["MotCle"]:
        self.cursor.execute('''
            SELECT id FROM keywords
        ''')
        mot_cles = []
        for (id_espace,) in self.cursor.fetchall():
            motcle = MotCle.load(id_espace, self)
            if motcle:
                mot_cles.append(motcle)
        return mot_cles

    def close(self):
        self.conn.close()