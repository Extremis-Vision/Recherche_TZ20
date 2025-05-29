import chromadb
from typing import List, Optional
from chromadb.utils import embedding_functions

class ChromaDB:
    def __init__(self, url: str, port : int, username: str, mdp: str, collection_name: str):
        self.username = username  # � adapter selon le mode (persistant ou non)
        self.mdp = mdp           # � adapter selon le mode (persistant ou non)
        self.collection_name = collection_name
        # Cr�ation du client ChromaDB
        self.client = chromadb.HttpClient(host=url, port=port)  # � ajuster selon ton URL
        # Tu peux aussi utiliser chromadb.Client() pour le mode in-memory
        # Cr�ation ou r�cup�ration de la collection
        # Pour un exemple avec un embedding function externe, voir ci-dessous
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name
            # embedding_function=...  # � ajouter si tu veux un embedding function custom
        )

    def add_document(self, document: str, embedding: List[float], doc_id: Optional[str] = None):
        """
        Ajoute un document � la collection, avec son embedding.
        :param document: Texte du document
        :param embedding: Vecteur d'embedding calcul�
        :param doc_id: Identifiant unique du document (optionnel)
        """
        if doc_id is None:
            doc_id = f"doc_{len(self.collection.get().get('ids', [])) + 1}"
        self.collection.add(
            documents=[document],
            embeddings=[embedding],
            ids=[doc_id]
        )

    def add_documents(self, documents: List[str], embeddings: List[List[float]], doc_ids: Optional[List[str]] = None):
        """
        Ajoute plusieurs documents � la collection, avec leurs embeddings.
        :param documents: Liste de textes
        :param embeddings: Liste de vecteurs d'embedding
        :param doc_ids: Liste d'identifiants uniques (optionnel)
        """
        if doc_ids is None:
            doc_ids = [f"doc_{i+1}" for i in range(len(documents))]
        self.collection.add(
            documents=documents,
            embeddings=embeddings,
            ids=doc_ids
        )
