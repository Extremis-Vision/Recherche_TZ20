import sys, os 

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from typing import List, Dict
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
from Recherche.SimpleSearch import SimpleSearch
from dotenv import load_dotenv
import requests
import json

load_dotenv()
SEARCHURL = os.getenv("SEARCHURL")

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
    
    def search_results_deep(self, query: str, engines: List[str] = None, categories: List[str] = None, acceptScore: float = 0.5, num_results: int = 5) -> List[Dict]:
        """
        Effectue une requête de recherche via l'API SearchX et renvoie les résultats avec 'snippet' au lieu de 'content'.
        """
        params = {
            'q': query,
            'engines': ','.join(engines) if engines else None,
            'categories': ','.join(categories) if categories else None,
            'format': 'json',
        }
        params = {k: v for k, v in params.items() if v is not None}

        response = requests.get(SEARCHURL, params=params)

        if response.status_code == 200:
            resultats = response.json()
            results = []

            for i in resultats.get("results", []):
                if i.get("score", 0) >= acceptScore:
                    # On copie le dict et on renomme 'content' en 'snippet'
                    item = i.copy()
                    if 'content' in item:
                        item['snippet'] = item.pop('content')
                    results.append(item)
                if len(results) >= num_results:
                    break

            # Sauvegarde pour debug
            with open('search_results.json', 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)

            return results

        else:
            print(f"Erreur: {response.status_code}, {response.text}")
            return []

    def multiplesearch_deep(self, keywords: List[str], num_results: int = 5, engines: List[str] = None, categories: List[str] = None, acceptScore: float = 0.5) -> List[Dict]:
        """
        Effectue une recherche pour chaque mot-clé, agrège et retourne tous les résultats avec 'snippet' au lieu de 'content'.
        """
        all_results = []
        for keyword in keywords:
            res = self.search_results_deep(
                query=keyword,
                engines=engines,
                categories=categories,
                acceptScore=acceptScore,
                num_results=num_results
            )
            all_results.extend(res)
        return all_results


#Exemple utilisation de RechercheCrawling
#urls = ["https://sbert.net/"]
#resultat_recherche = RechercheCrawling()
#docs = resultat_recherche.multiplesearch_deep(["Crawler"])

#from Generation.ChromaDB import ChromaDB
#chroma_db = ChromaDB()
#chroma_db.add_documents_deepsearch(docs)


