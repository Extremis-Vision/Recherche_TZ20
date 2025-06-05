import sys, os 

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Generation.ChromaDB import ChromaDB
from Recherche.RechercheBasique import RechercheBasique

# Example usage
if __name__ == "__main__":
    chroma_db = ChromaDB()
    recherche = RechercheBasique()

    # Nettoyer la collection avant d'ajouter de nouveaux documents
    #chroma_db.clear_collection()

    # Faire la recherche et ajouter les résultats
    search_query = "Charles de Gaulle"
    recherche_results = recherche.search_results(search_query, num_results=10)
    print("Résultats de la recherche :", recherche_results)
    
    if recherche_results:
        chroma_db.add_documents(recherche_results)
        
        # Vérifier les documents ajoutés avec la même requête
        found_docs = chroma_db.get_documents(n_results=5, query=search_query)
        print("\nDocuments trouvés pour la requête :", search_query)
        for doc in found_docs:
            print("Titre:", doc["title"])
            print("Lien:", doc["link"])
            print("Snippet:", doc["snippet"])
            print("---")
    else:
        print("Aucun résultat trouvé")
