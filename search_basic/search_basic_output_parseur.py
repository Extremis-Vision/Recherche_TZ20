from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from typing import List
import csv
import os

# Étape 1: Définir la structure de sortie avec Pydantic
class QueryResponse(BaseModel):
    querys: List[str] = Field(description="Liste de 5 mots-clés de recherche en anglais")
    categories: str = Field(description="Catégorie principale de la recherche")

# Étape 2: Initialiser le parser
parser = PydanticOutputParser(pydantic_object=QueryResponse)

# Étape 3: Créer le prompt avec instructions de formatage
system_prompt = """Tu es un assistant de recherche qui doit générer des mots clés qui seront utilisés dans un moteur de recherche. 
Fais en sorte que ces mots clés représentent au mieux ce qui serait nécessaire à la recherche. 
Donne uniquement les mots clés et rien d'autre en anglais. Génère exactement 5 mots clés.

Format de réponse requis :
{format_instructions}"""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("user", "{input}")
])

models_list = ["granite-3.2-8b-instruct","gemma-3-12b-it","mathstral-7b-v0.1","ministral-8b-instruct-2410","gemma-3-4b-it","qwq-lcot-7b-instruct"]
models = "granite-3.2-8b-instruct"

# Étape 4: Configurer le modèle local
model = ChatOpenAI(
    api_key="lm-studio",
    base_url="http://localhost:1234/v1",
    model=models,
    temperature=0.7,
    max_tokens=4096
)

# Étape 5: Créer la chaîne de traitement
chain = prompt | model | parser

# Étape 6: Exécuter avec gestion d'erreurs
def get_structured_response(question: str):
    try:
        response = chain.invoke({
            "input": question,
            "format_instructions": parser.get_format_instructions()
        })
        return response
    except Exception as e:
        print(f"Erreur de parsing : {e}")
        return None

# Utilisation
if __name__ == "__main__":
    question = "Pourquoi n'utilise t'on pas les réseaux de neurones convolutifs pour les LLMs ?"
    score = 0
    results = []

    attempts = 100

    for i in range(attempts):
        print(f"\nRéponse {i+1}:")
        result = get_structured_response(question)
        if result:
            if (result.querys and result.categories) is not None:
                score += 1
                print(f"Mots-clés : {result.querys}")
                print(f"Catégorie : {result.categories}")
            results.append(result)

    print(f"Score : {score}")
    fieldnames = ['model_name', "attempts", 'score', "result"]

    # Check if file exists to determine mode and header writing
    file_exists = os.path.isfile('benchmark.csv')

    with open('benchmark.csv', 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write header only if file is new
        if not file_exists:
            writer.writeheader()
        
        # Write the new row
        writer.writerow({
            'model_name': models,
            "attempts": attempts,
            'score': score,
            "result": str(results)
        })

    print("Results appended to benchmark.csv")

