import requests
from pprint import pprint

def fetch_searx_results(query, host="http://localhost:4000", limit=20):
    params = {
        "q": query,
        "format": "json",
        "pageno": 1,
        "time_range": "year",  # Filtre temporel optionnel
        "engines": "bing,wikipedia"  # S�lection des moteurs
    }
    response = requests.get(f"{host}/search", params=params)
    return response.json()['results'][:limit]

results = fetch_searx_results("Large Language Model")
pprint(results)