import sys, os 

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from typing import List, Dict
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
from Recherche.SimpleSearch import SimpleSearch

class RechercheCrawling(SimpleSearch):        
    async def crawl_url_and_update(self, doc: Dict, max_retries: int = 3) -> Dict:
        run_conf = CrawlerRunConfig(cache_mode=CacheMode.BYPASS, stream=True)
        url = doc.get('link')
        if not url:
            doc['markdown'] = None
            return doc

        for attempt in range(1, max_retries + 1):
            try:
                async with asyncio.timeout(10):  # Timeout de 10 secondes
                    async with AsyncWebCrawler() as crawler:
                        result = await crawler.arun(url, config=run_conf)
                        if result.success:
                            doc['markdown'] = result.markdown.raw_markdown
                            return doc
                        else:
                            print(f"Erreur lors du crawl de {url} (tentative {attempt})")
            except asyncio.TimeoutError:
                print(f"Timeout: Le crawl de {url} a pris plus de 10 secondes (tentative {attempt})")
            except Exception as e:
                print(f"Erreur inattendue lors du crawl de {url} (tentative {attempt}): {e}")
            # Petite pause entre les tentatives pour ne pas spammer
            await asyncio.sleep(1)

        # Si toutes les tentatives échouent
        doc['markdown'] = None
        return doc

    def get_websites_content(self, docs: List[Dict], limit: int = 3, max_retries: int = 3) -> List[Dict]:
        """
        Pour chaque dict de la liste, ajoute la clé 'markdown' avec le contenu crawlé.
        Si un crawl échoue, il retente jusqu'à max_retries fois, puis passe au suivant.
        """
        async def crawl_all(docs_to_crawl):
            tasks = [self.crawl_url_and_update(doc, max_retries=max_retries) for doc in docs_to_crawl]
            return await asyncio.gather(*tasks)

        docs_to_crawl = docs[:limit]
        return asyncio.run(crawl_all(docs_to_crawl))


#Exemple utilisation de RechercheCrawling
#urls = ["https://sbert.net/"]
#resultat_recherche = RechercheCrawling()
#print(resultat_recherche.get_websites_contend(urls))

from Recherche.RechercheBasique import RechercheBasique

resultat_recherche = RechercheBasique()

docs = resultat_recherche.multiplesearch(
                ["Output parser"],
                5
            )

crawling = RechercheCrawling()
result = crawling.get_websites_content(docs, limit=5)

print(result)