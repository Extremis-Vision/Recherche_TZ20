import requests
import json
import os
import time
import requests
from bs4 import BeautifulSoup
import time

SEARCHURL = "http://localhost:4000/search"

def search_query(query, engines=None, categories=None):
    """
    Effectue une requ�te de recherche via l'API SearchX.

    :param query: La requète de recherche.
    :param engines: Liste des moteurs à utiliser (optionnel).
    :param categories: Liste des catégories à activer (optionnel).
    :return: Résultats de la recherche au format JSON.
    """
    params = {
        'q': query,
        'engines': ','.join(engines) if engines else None,
        'categories': ','.join(categories) if categories else None,
        'format': 'json',  # Format des r�sultats
    }
    
    response = requests.get(SEARCHURL, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erreur: {response.status_code}, {response.text}")
        return None
    

def research(search_subject):
    resultats = search_query(search_subject, engines=["google", "bing"], categories=["science"])
    print(resultats)

    with open('search_results.json', 'w', encoding='utf-8') as f:
        json.dump(resultats, f, ensure_ascii=False, indent=2)
    print("Results saved to search_results.json")

    results = []

    with open('search_results.json', 'r', encoding='utf-8') as f:
        resultat = json.load(f)
        for result in resultat["results"]:
            results.append(result["title"])

    return results

def scrapeur(lien):
    try:

        response = requests.get(lien, timeout=100)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        return soup
    
    except Exception as e:
        print(f"Erreur : {str(e)}")
        return []


print(scrapeur("https://muse.jhu.edu/pub/3/article/524814/summary"))
