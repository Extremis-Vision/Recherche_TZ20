from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from typing import List
import csv
import os
import sys

# Add the parent directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from searchX import research

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
models = "gemma-3-12b-it"

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
    result = get_structured_response(question)
    results = []

    if result:
        if (result.querys and result.categories) is not None:
            print(f"Mots-clés : {result.querys}")
            print(f"Catégorie : {result.categories}")

            for subject in result.querys:
                temp = research(subject)
                results.append(temp)

    #print("Résultats de recherche :", results)