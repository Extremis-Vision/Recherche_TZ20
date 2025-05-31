import os
import chromadb
from chromadb.config import Settings
from typing import List, Optional
from dotenv import load_dotenv
import numpy as np
import lmstudio as lms

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

    def name(self):
        return "nomic-embed-text-v1.5"

class ChromaDB:
    def __init__(self, embedding_function=None):
        self.host = os.getenv("CHROMA_SERVER_HOST", "localhost")
        self.port = int(os.getenv("CHROMA_SERVER_PORT", "8000"))
        self.token = os.getenv("CHROMA_SERVER_AUTH_CREDENTIALS", "")
        self.collection_name = os.getenv("CHROMA_COLLECTION_NAME", "nomic_collection")

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
        """
        Ajoute des documents à la collection ChromaDB.
        """
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
            print(f"Added {len(documents)} documents to the collection.")

    def get_documents(self, n_results: int = 5, query: str = None) -> List[dict]:
        """
        Récupère les documents pertinents pour la query.
        """
        docs = []
        if query:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            metadatas = results['metadatas'][0] if results.get('metadatas') else []
            print(f"Found {len(metadatas)} documents for the query: {query}")
        else:
            results = self.collection.get(limit=n_results)
            metadatas = results['metadatas'] if results.get('metadatas') else []
            print(f"Retrieved {len(metadatas)} documents without a query.")

        for meta in metadatas:
            docs.append({
                "title": meta.get("title"),
                "link": meta.get("link"),
                "snippet": meta.get("snippet")
            })
        return docs

    def clear_collection(self):
        """
        Supprime tous les documents de la collection.
        """
        results = self.collection.get()
        ids = results['ids'] if results and 'ids' in results else []

        if ids:
            self.collection.delete(ids=ids)
            print(f"Deleted {len(ids)} documents from the collection.")
        else:
            print("No documents to delete.")

    def response_with_context(self, prompt: str, NB_result_use=5, model_name: str = "ministral-8b-instruct-2410") -> Optional[str]:
        """
        Génère une réponse à partir du contexte extrait des documents pertinents.
        """
        # 1. Recherche des documents pertinents
        docs = self.get_documents(n_results=NB_result_use, query=prompt)
        if not docs:
            return "Aucune information pertinente trouvée dans la base de connaissances."

        # 2. Construction du contexte formaté et limité en taille
        context_blocks = []
        total_tokens = 0
        max_tokens = 2048  # Adapte selon la capacité de ton modèle
        for doc in docs:
            block = (
                f"\nSource: {doc['title']}\n"
                f"Snippet: {doc['snippet']}\n"
                f"Lien: {doc['link']}\n"
            )
            block_tokens = len(block.split())  # Approximation simple
            if total_tokens + block_tokens > max_tokens:
                break
            context_blocks.append(block)
            total_tokens += block_tokens
        context = "\n".join(context_blocks)

        # 3. Prompt system amélioré
        system_prompt = f"""
        You must generate a response using only the context provided below, and you must cite the sources of any information you use.
        Your response must be in the same language as the user's input.
        Citation format:
        At the end of each paragraph that uses information from a source, add the following citation format: (source_name)[link]

        Example:
        [datascientest.com](https://datascientest.com/transformer-models-tout-savoir)

        Instructions:
        - Use only the provided context to answer the user's question.
        - Ignore any context that does not answer the question.
        - Do not use any external information or sources.
        - For every factual statement or paragraph that uses information from the context, cite the relevant source in the specified format.
        - Write your response in the same language as the user's input.
        - Do not invent or hallucinate sources.
        - Only respond to the user query no more no less, but always source what you say in the user query language.
        - If you are not capable to respond correctly, just say what you lack of.

        Context to use:
        {context}
        """

        try:
            model = lms.llm(model_name)
            chat = lms.Chat(system_prompt)
            chat.add_user_message(prompt)

            prediction_stream = model.respond_stream(chat)
            for fragment in prediction_stream:
                yield fragment.content
        except Exception as e:
            print(f"Erreur lors de la génération de la réponse : {e}")
            return None
