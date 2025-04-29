import pandas as pd
import json
from ast import literal_eval
import numpy as np

# Charger le fichier JSON
with open('/home/ghost/Documents/function_calling/3_analyse_result/benchmark_structured_output.json') as f:
    data = json.load(f)

# Analyse pour chaque modèle dans les résultats
for model_data in data["results"]:
    print(f"\n=== Analyse pour le modèle {model_data['model_name']} ===")
    
    # Statistiques sur les temps
    times = {k: v for item in model_data['time'] for k, v in item.items()}
    print("\nStatistiques de temps:")
    print(f"Temps de chargement: {times['chargement_model']:.2f}s")
    print(f"Temps moyen de réponse: {times['avg_reponse_time']:.2f}s")
    print(f"Temps total: {times['total_time']:.2f}s")
    
    # Scores
    print(f"\nScores: {model_data['score']}")
    print(f"Score moyen: {np.mean(model_data['score']):.2f}")

    # Analyse des résultats
    results = model_data["result"]
    if isinstance(results, str):
        try:
            # Utiliser json.loads au lieu de literal_eval
            results = json.loads(results)
        except json.JSONDecodeError:
            print(f"Erreur de parsing JSON pour le modèle {model_data['model_name']}")
            continue

    df = pd.json_normalize(results)
    
    # Filtrer les entrées valides (sans erreur)
    df_valid = df[df['categories'].notna()]
    
    if not df_valid.empty:
        # Explode pour séparer les listes de mots-clés
        df_exploded = df_valid.explode('mot_cle')
        
        # Statistiques sur les catégories
        print("\nDistribution des catégories:")
        category_counts = df_valid['categories'].str.lower().str.strip().value_counts()
        print(category_counts)
        
        # Statistiques sur les mots-clés
        print("\nTop 10 des mots-clés les plus fréquents:")
        keyword_counts = df_exploded['mot_cle'].str.lower().str.strip().value_counts().head(10)
        print(keyword_counts)
        
        # Nombre total d'entrées valides
        print(f"\nNombre total d'entrées valides: {len(df_valid)}")
        
    # Nombre d'erreurs si présentes
    if 'Erreur' in df.columns:
        errors = df[df['Erreur'].notna()]
        if not errors.empty:
            print(f"\nNombre d'erreurs: {len(errors)}")
            print("Types d'erreurs:")
            print(errors['Erreur'].value_counts())

    print("\n" + "="*50)

