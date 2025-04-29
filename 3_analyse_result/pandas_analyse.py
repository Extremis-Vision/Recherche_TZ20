import pandas as pd
import ast

# Chargement des données
df = pd.read_csv('/home/ghost/Documents/function_calling/3_analyse_result/benchmark_structured_output.csv')

print(df.head())


# Conversion des colonnes JSON
test = df['time'].apply(ast.literal_eval)
print(test)

#df['time'] = df['time'].apply(ast.literal_eval)
#df['result'] = df['result'].apply(ast.literal_eval)

# Feature engineering
#df['temps_reponse_moyen'] = df['time'].apply(lambda x: (x['end_time'] - x['chargement_model']) / len(x) / 10)
 