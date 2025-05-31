# Example usage
if __name__ == "__main__":
    snippets = [{'title': 'Bonjour .com a votre service', 'link': 'https://en.wikipedia.org/wiki/Transformer_(deep_learning_architecture)', 'snippet': 'Transformer is a neural network ...'}]
    chroma_db = ChromaDB()

    # Clear the collection before adding new documents
    chroma_db.clear_collection()

    # Add documents
    chroma_db.add_documents(snippets)

    # V�rification des documents ajout�s
    all_docs = chroma_db.get_documents(n_results=1000)
    print("Documents ajout�s :")
    for doc in all_docs:
        print("Titre:", doc["title"])
        print("Lien:", doc["link"])
        print("Snippet:", doc["snippet"])
        print("---")

    # Recherche de documents pertinents
    important_docs = chroma_db.get_documents(n_results=5, query="Bonjour .com")
    print("Documents pertinents pour la requ�te 'Bonjour .com' :")
    for doc in important_docs:
        print("Titre:", doc["title"])
        print("Lien:", doc["link"])
        print("Snippet:", doc["snippet"])
        print("---")
