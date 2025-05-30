import requests
import json
import asyncio
from typing import List, Dict
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
from .RechercheBasique import RechercheBasique

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

#Exemple utilisation de RechercheCrawling
#urls = ["https://sbert.net/"]
#resultat_recherche = RechercheCrawling()
#print(resultat_recherche.get_websites_contend(urls))