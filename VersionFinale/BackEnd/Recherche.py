import requests
import json
import asyncio
from typing import List, Optional, Dict, Any
from dotenv import load_dotenv
import os
from langchain_community.utilities import SearxSearchWrapper
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode

load_dotenv()
SEARCHURL = os.getenv("SEARCHURL")

class RechercheBasique:
    def __init__(self):
        self.search = SearxSearchWrapper(searx_host=SEARCHURL)
        self.model = model

    def search_results(self, query: str, engines: List[str] = None, num_results: int = 5) -> List[Dict]:
        """
        Effectue une recherche simple sur les moteurs de recherche.
        :param query: Requ�te de recherche
        :param engines: Liste des moteurs (ex: ['wikipedia', 'bing', 'google'])
        :param num_results: Nombre de r�sultats � retourner
        :return: Liste de r�sultats au format dict
        """
        if engines is None:
            engines = ['wikipedia', 'bing', 'yahoo', 'google', 'duckduckgo']
        return self.search.results(query, engines=engines, num_results=num_results)

    def get_info(self, query: str, engines: List[str] = None, num_results: int = 5) -> List[Dict]:
        """
        Retourne les r�sultats bruts de la recherche.
        :param query: Requ�te de recherche
        :param engines: Liste des moteurs (optionnel)
        :param num_results: Nombre de r�sultats � retourner
        :return: Liste de r�sultats au format dict
        """
        return self.search_results(query, engines, num_results)

class RechercheCrawling:
    def __init__(self, model: str = "ministral-8b-instruct-2410"):
        self.model = model

    async def crawl_urls(self, urls: List[str]) -> List[Dict]:
        """
        Crawle une liste d?URLs et retourne le contenu au format Markdown.
        :param urls: Liste d?URLs � crawler
        :return: Liste de dictionnaires {'url': ..., 'markdown': ...}
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

    def get_website_info(self, urls: List[str], limit: int = 3) -> List[Dict]:
        """
        Retourne le contenu Markdown d?une liste d?URLs (synchrone).
        :param urls: Liste d?URLs � crawler
        :param limit: Nombre maximal d?URLs � traiter
        :return: Liste de dictionnaires {'url': ..., 'markdown': ...}
        """
        data = []
        for url in urls[:limit]:
            data += asyncio.run(self.crawl_urls([url]))
        data = [d for d in data if d.get("markdown")]
        if not data:
            print("Aucun contenu Markdown r�cup�r�.")
        return data
