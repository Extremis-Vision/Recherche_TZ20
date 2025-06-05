import sys, os 

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Generation.ChromaDB import ChromaDB

# Example usage
if __name__ == "__main__":
    chroma_db = ChromaDB()

    # V�rification des documents ajout�s
    all_docs = chroma_db.get_documents(n_results=1000)
    print("Documents ajout�s :")
    for doc in all_docs:
        print("Titre:", doc["title"])
        print("Lien:", doc["link"])
        print("Snippet:", doc["snippet"])
        print("---")

    # Recherche de documents pertinents
    important_docs = chroma_db.get_documents(n_results=5, query="faillite entreprise France")
    print("Documents pertinents pour la requ�te 'Bonjour .com' :")
    for doc in important_docs:
        print("Titre:", doc["title"])
        print("Lien:", doc["link"])
        print("Snippet:", doc["snippet"])
        print("---")
