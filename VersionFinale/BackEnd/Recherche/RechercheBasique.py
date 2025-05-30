from typing import List, Dict
from dotenv import load_dotenv
import os
from langchain_community.utilities import SearxSearchWrapper

load_dotenv()
SEARCHURL = os.getenv("SEARCHURL")

class RechercheBasique:
    def __init__(self,engines : List[str] = None):
        self.search = SearxSearchWrapper(searx_host=SEARCHURL)
        if engines == None:
            self.engines = ['wikipedia', 'bing', 'yahoo', 'google', 'duckduckgo']
        else :
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

# Exemple utilisation de RechercheBasique
#resultat_recherche = RechercheBasique()
#print(resultat_recherche.search_results("Transformer",10))
