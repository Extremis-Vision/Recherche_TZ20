import pandas as pd
import json
from ast import literal_eval

# Chargement du JSON
with open('/home/ghost/Documents/function_calling/3_analyse_result/becnhmark_structured_output.json') as f:
    data = json.load(f)

# Conversion en DataFrame
df = pd.json_normalize(data['results'])

# Nettoyage des colonnes
df['result'] = df['result'].apply(literal_eval)
df['score'] = df['score'].apply(lambda x: sum(x)/len(x))  # Moyenne des scores
df['time_metrics'] = df['time'].apply(lambda x: {k:v for d in x for k,v in d.items()})

print(df.columns)

# Extraction des métriques temporelles
time_df = pd.json_normalize(df['time_metrics'])
df = pd.concat([df, time_df], axis=1)

# Calcul du débit (tokens/seconde)
df['throughput'] = df['max_tokens'] / df['avg_reponse_time']

# Découpage des résultats
df = df.explode('result').reset_index(drop=True)
