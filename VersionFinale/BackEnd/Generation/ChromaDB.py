import os
import chromadb
from chromadb.config import Settings
from typing import List, Optional, Union
from dotenv import load_dotenv

# Charge les variables d'environnement
load_dotenv(os.path.join('..', '.env'))

class ChromaDB:
    def __init__(
        self,
        embedding_function=None,  # Peut �tre une fonction d'embedding personnalis�e ou None pour utiliser la fonction par d�faut
    ):
        self.host = os.getenv("CHROMA_SERVER_HOST", "localhost")
        self.port = os.getenv("CHROMA_SERVER_PORT", "8000")
        self.token = os.getenv("CHROMA_SERVER_AUTH_CREDENTIALS", "")
        self.collection_name = os.getenv("CHROMA_COLLECTION_NAME", "default_collection")

        # Configuration du client ChromaDB avec authentification par token
        self.client = chromadb.HttpClient(
            host=self.host,
            port=self.port,
            settings=Settings(
                chroma_client_auth_provider="chromadb.auth.token.TokenAuthClientProvider",
                chroma_client_auth_credentials=self.token
            )
        )

        # Cr�ation ou r�cup�ration de la collection
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            embedding_function=embedding_function  # Utilise la fonction d'embedding fournie
        )
