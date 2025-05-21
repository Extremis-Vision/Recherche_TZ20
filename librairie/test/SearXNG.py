import requests
import json
import os
import time
import requests
from bs4 import BeautifulSoup
import time
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
import sys
from typing import List
import RAG
import readyOutputParser


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
    resultats = search_query(search_subject, engines=['wikipedia', 'bing', 'yahoo', 'google', 'duckduckgo'])
    results = []

    for i in resultats["results"]:
        if i["score"] >= 0.5:
            results.append(i["url"])

    with open('search_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    return results  

async def parallel_crawl_async(urls):
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


def crawler(urls, model : str = "gemma-3-12b-it-qat"):
    data =[]
    for url in urls[:3]:
        data += asyncio.run(parallel_crawl_async([url]))
        print("Passe au suivant")
    data = [d for d in data if d.get("markdown")]
    if not data:
        print("Aucun contenu Markdown récupéré, impossible de créer les embeddings.")
        return
    print("RAG ")
    RAG.RAG(data, model)


def ai_research(question: str, model : str = "gemma-3-12b-it-qat"):
    key_words = readyOutputParser.get_key_word(question, model)
    urls = []
    print(key_words)
    for word in key_words[0]:
        result = research(word)
        if isinstance(result, list):
            urls.extend(result)
        else:
            urls.append(result)
    # Filtre les URLs PDF et vides
    flattened_urls = [u for u in urls if u and isinstance(u, str) and not u.lower().endswith('.pdf')]
    crawler(flattened_urls, model)


ai_research("Qu'est ce qu'un transformer", "ministral-8b-instruct-2410")
