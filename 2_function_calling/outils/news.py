import feedparser
import json

def get_data():
    with open('./data/url_journal_rss.json', 'r') as f:
        return json.load(f)

def actualite_rss(rss_url):
    # Parser le flux RSS
    feed = feedparser.parse(rss_url)

    # Parcourir les entr�es du flux RSS (articles)
    dico_actu_journal = {}

    for entry in feed.entries:
        # Titre de l'article
        dico_actu_journal[entry.title] = {"url": entry.link, "description": entry.description}

    return dico_actu_journal

def actualite(demande_0, demande_1=None):
    dico_flux_rss = get_data()

    if demande_0 in dico_flux_rss:
        if demande_1 and demande_1 in dico_flux_rss[demande_0]:
            # Si demande_1 est sp�cifi�, retourne les actualit�s pour cette cl�
            return actualite_rss(dico_flux_rss[demande_0][demande_1])
        else:
            # Sinon, retourne une liste de toutes les actualit�s pour demande_0
            liste = []
            for key in dico_flux_rss[demande_0]:
                liste.append(actualite_rss(dico_flux_rss[demande_0][key]))
            return liste
    else:
        return "error"


#print(actualite("crypto"))