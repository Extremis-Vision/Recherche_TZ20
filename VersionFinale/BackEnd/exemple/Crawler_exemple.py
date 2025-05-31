
from Recherche.RechercheBasique import RechercheBasique

resultat_recherche = RechercheBasique()

docs = resultat_recherche.multiplesearch(
                ["Output parser"],
                5
            )

crawling = RechercheCrawling()
result = crawling.get_websites_content(docs, limit=5)

print(result)