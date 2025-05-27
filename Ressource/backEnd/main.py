import generation as gen
import recherche as rec


question = "Est ce que NeoJ4 permet d'enregistrer des données normalement ?"
keywords = gen.get_key_word_search(question,3)
print(keywords)

rec.simple_search(question)
