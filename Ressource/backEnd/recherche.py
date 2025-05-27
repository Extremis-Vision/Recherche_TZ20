import requests
import json
import requests
import time
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
from typing import List
import generation as gen
from dotenv import load_dotenv
import os
from langchain_community.utilities import SearxSearchWrapper
import lmstudio as lms
import retrieveAugmentedGeneration as rg

load_dotenv()
SEARCHURL = os.getenv("SEARCHURL")
search = SearxSearchWrapper(searx_host= SEARCHURL)

def simple_search(question : str, model : str = "ministral-8b-instruct-2410", engines :List[str] = ['wikipedia', 'bing', 'yahoo', 'google', 'duckduckgo'], num_results : int = 10, keywords : List[str] = None):
    results = []
    for keyword in (keywords or gen.get_key_word_search(question, 1)):
        results.extend(search.results(keyword, engines, num_results))
    return gen.response_with_context(question, str(results), model, keywords[1])


def get_search_info(query : str, engines : str = None, categories : str  = None, acceptScore : int = 0.5):
    """
    Effectue une requete de recherche via l'API SearchX.

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
        resultats =  response.json()
        results = []

        for i in resultats["results"]:
            if i["score"] >= acceptScore:
                results.append(i["url"])

        with open('search_results.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        return results  

    else:
        print(f"Erreur: {response.status_code}, {response.text}")
        return None

async def Crawler(urls : List[str]):
    """
    Effectue un traitement des urls et récupère les données de ceux-ci.

    :param query: La requète de recherche.
    :param engines: Liste des moteurs à utiliser (optionnel).
    :param categories: Liste des catégories à activer (optionnel).
    :return: Résultats de la recherche au format JSON.
    """
    run_conf = CrawlerRunConfig(cache_mode=CacheMode.BYPASS, stream=True)
    results = []
    total = len(urls)
    async with AsyncWebCrawler() as crawler:
        idx = 1
        async for result in await crawler.arun_many(urls, config=run_conf):
            if result.success:
                print(f"[{idx}/{total}] URL: {result.url} - Markdown length: {len(result.markdown.raw_markdown)}")
                results.append({
                    "url": result.url,
                    "markdown": result.markdown.raw_markdown,
                })
            else:
                print(f"[{idx}/{total}] Error crawling {result.url}: {result.error_message}")
            idx += 1
    return results



def get_website_info(urls : List[str], model : str = "ministral-8b-instruct-2410" , limit : int = 3):
    data =[]
    for url in urls[:limit]:
        data += asyncio.run(Crawler([url]))
        print("Passe au suivant")
    data = [d for d in data if d.get("markdown")]
    if not data:
        print("Aucun contenu Markdown récupéré, impossible de créer les embeddings.")
        return
    return data

def deepsearch(question: str, model : str = "ministral-8b-instruct-2410"):
    key_words = gen.get_key_word_deepsearch(question, model)
    urls = []
    print(key_words)
    for word in (key_words["KeywordSubjectDef"] and key_words["SpecificKeyWord"]):
        result = get_search_info(word)
        if isinstance(result, list):
            urls.extend(result)
        else:
            urls.append(result)
    
    print(urls)
    flattened_urls = [u for u in urls if u and isinstance(u, str) and not u.lower().endswith('.pdf')]
    data = get_website_info(flattened_urls, model, 20)
    print(search.results(gen.get_key_word_search(question,1), engines=['wikipedia', 'bing', 'yahoo', 'google', 'duckduckgo'], num_results=5))
    rg.get_RAG_response(data,question,5,model)


# Modifier la fonction de rechercher en penant en compte : https://github.com/rashadphz/farfalle
# Refaire le RAG pour l'optimiser avec LlamaIndex ou Langchain

#print(simple_search("C'est quoi Crawl4AI ?")) 