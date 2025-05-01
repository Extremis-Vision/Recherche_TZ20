import pandas as pd
import json
from ast import literal_eval

# Charger le fichier JSON
with open('/home/ghost/Documents/function_calling/3_analyse_result/benchmark_structured_output.json') as f:
    data = json.load(f)


    results = data["results"][4]["result"]

    # Convertir les chaînes JSON en objets Python si nécessaire
    if isinstance(results, str):
        results = literal_eval(results.replace("'", "\""))

    df = pd.json_normalize(results)

    # Explode pour séparer les listes de mots-clés
    df_exploded = df.explode('mot_cle')

    # Compter les catégories
    category_counts = df['categories'].str.lower().str.strip().value_counts()

    # Compter les mots-clés
    keyword_counts = df_exploded['mot_cle'].str.lower().str.strip().value_counts()

    print("Catégories :\n", category_counts)
    print("\nMots-clés :\n", keyword_counts)

