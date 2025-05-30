import os
import chromadb
from chromadb.config import Settings
from typing import List
from dotenv import load_dotenv
import numpy as np

# Load environment variables from .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

class NomicEmbeddingFunction:
    def __init__(self):
        try:
            import lmstudio as lms
            self.model = lms.embedding_model("nomic-embed-text-v1.5")
        except ImportError:
            print("lmstudio not found. Using mock embedding function.")
            self.model = None

    def __call__(self, input: List[str]) -> List[np.ndarray]:
        if self.model is not None:
            return [np.array(self.model.embed(text)) for text in input]
        else:
            # Mock embedding function
            return [np.array([0.1 * i] * 5) for i in range(len(input))]

class ChromaDB:
    def __init__(self, embedding_function=None):
        self.host = os.getenv("CHROMA_SERVER_HOST", "localhost")
        self.port = int(os.getenv("CHROMA_SERVER_PORT", "8000"))
        self.token = os.getenv("CHROMA_SERVER_AUTH_CREDENTIALS", "")
        self.collection_name = os.getenv("CHROMA_COLLECTION_NAME", "default_collection")

        if embedding_function is None:
            embedding_function = NomicEmbeddingFunction()

        self.client = chromadb.HttpClient(
            host=self.host,
            port=self.port,
            settings=Settings(
                chroma_client_auth_credentials=self.token,
                chroma_auth_token_transport_header="Authorization"
            )
        )

        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            embedding_function=embedding_function
        )

    def add_documents(self, docs: List[dict]):
        documents = []
        metadatas = []
        ids = []

        for i, doc in enumerate(docs):
            title = doc.get("title")
            link = doc.get("link")
            snippet = doc.get("snippet", "")
            if not title or not link:
                continue

            documents.append(f"{title}. {snippet}")
            metadatas.append({
                "link": link,
                "title": title,
                "snippet": snippet
            })
            ids.append(f"doc_{i}")

        if documents:
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )

    def get_documents(self, n_results: int = 5, query: str = None) -> List[dict]:
        if query:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            metadatas = results['metadatas'][0] if results['metadatas'] else []
        else:
            metadatas = self.collection.peek(n_results=n_results)['metadatas']

        docs = []
        for meta in metadatas:
            docs.append({
                "title": meta.get("title"),
                "link": meta.get("link"),
                "snippet": meta.get("snippet")
            })
        return docs

# Example usage
if __name__ == "__main__":
    snippets = [
        {
            'title': 'Transformer (deep learning architecture) - Wikipedia',
            'link': 'https://en.wikipedia.org/wiki/Transformer_(deep_learning_architecture)',
            'snippet': 'Transformer is a neural network ...'
        }
    ]

    chroma_db = ChromaDB()
    chroma_db.add_documents(snippets)

    important_docs = chroma_db.get_documents(n_results=5, query="Qu'est-ce qu'un Transformer ?")
    for doc in important_docs:
        print("Titre:", doc["title"])
        print("Lien:", doc["link"])
        print("Snippet:", doc["snippet"])
        print("---")
