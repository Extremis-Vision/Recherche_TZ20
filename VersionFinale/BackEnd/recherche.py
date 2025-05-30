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
    def __init__(self,engines : List[str] = ['wikipedia', 'bing', 'yahoo', 'google', 'duckduckgo']):
        self.search = SearxSearchWrapper(searx_host=SEARCHURL)
        self.engines = engines

    def search_results(self, keyword: str, num_results: int = 5, engines: List[str] = None) -> List[Dict]:
        engines = engines if engines is not None else self.engines
        return self.search.results(keyword, engines=engines, num_results=num_results)

    def multiplesearch(self, keywords: List[str], num_results: int = 5, engines: List[str] = None ) -> List[Dict]:
        engines = engines if engines is not None else self.engines
        results = []
        for keyword in keywords:
            results.extends(self.search_results(keyword,num_results,engines))
        return results


class RechercheCrawling(RechercheBasique):        
    async def crawl_urls(self, url: str) -> List[Dict]:
        run_conf = CrawlerRunConfig(cache_mode=CacheMode.BYPASS, stream=True)
        try:
            async with asyncio.timeout(10):  # Timeout de 10 secondes
                async with AsyncWebCrawler() as crawler:
                    result = await crawler.arun(url, config=run_conf)
                    if result.success:
                        return [{
                            "url": result.url,
                            "markdown": result.markdown.raw_markdown
                        }]
                    else:
                        print(f"Erreur lors du crawl de {url}")
                        return []
        except asyncio.TimeoutError:
            print(f"Timeout: Le crawl de {url} a pris plus de 10 secondes.")
            return []
        except Exception as e:
            print(f"Erreur inattendue lors du crawl de {url}: {e}")
            return []




    def get_websites_contend(self, urls: List[str], limit: int = 3) -> List[Dict]:
        data = []
        for url in urls[:limit]:
            data += asyncio.run(self.crawl_urls(url))
        return data

        

# Exemple utilisation de RechercheBasique
#resultat_recherche = RechercheBasique()
#print(resultat_recherche.search_results("Transformer",10))

#Exemple utilisation de RechercheCrawling
#urls = ["https://sbert.net/"]
#resultat_recherche = RechercheCrawling()
#print(resultat_recherche.get_websites_contend(urls))