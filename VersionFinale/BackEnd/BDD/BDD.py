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
            CREATE TABLE IF NOT EXISTS images (
                id SERIAL PRIMARY KEY,
                image BYTEA
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

    def get_EspaceRecherches(self) -> List["RechercheEspace"]:
        self.cursor.execute('''
            SELECT id FROM recherche_espaces
        ''')
        espaces = []
        for (id_espace,) in self.cursor.fetchall():
            espace = RechercheEspace.load(id_espace, self)
            if espace:
                espaces.append(espace)
        return espaces
    
    def get_Recherches(self) -> List["MotCle"]:
        self.cursor.execute('''
            SELECT id FROM recherches
        ''')
        mot_cles = []
        for (id_espace,) in self.cursor.fetchall():
            motcle = MotCle.load(id_espace, self)
            if motcle:
                mot_cles.append(motcle)
        return mot_cles

    def get_MotCles(self) -> List["MotCle"]:
        self.cursor.execute('''
            SELECT id FROM keywords
        ''')
        mot_cles = []
        for (id_espace,) in self.cursor.fetchall():
            motcle = MotCle.load(id_espace, self)
            if motcle:
                mot_cles.append(motcle)
        return mot_cles

    def get_Images(self) -> List["MotCle"]:
        self.cursor.execute('''
            SELECT id FROM images
        ''')
        mot_cles = []
        for (id_espace,) in self.cursor.fetchall():
            motcle = MotCle.load(id_espace, self)
            if motcle:
                mot_cles.append(motcle)
        return mot_cles
    
    def get_Sources(self) -> List["MotCle"]:
        self.cursor.execute('''
            SELECT id FROM sources
        ''')
        mot_cles = []
        for (id_espace,) in self.cursor.fetchall():
            motcle = MotCle.load(id_espace, self)
            if motcle:
                mot_cles.append(motcle)
        return mot_cles

    def close(self):
        self.conn.close()