from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from typing import List
from json_add import add_json
from ask_ai import get_model
import os
import time 
import re



def get_structured_response(question: str, models : str):
    class QueryResponse(BaseModel):
        querys: List[str] = Field(description="Liste de 5 mots-clés de recherche en anglais")
        categories: str = Field(description="Catégorie principale de la recherche")

    # Étape 2: Initialiser le parser
    parser = PydanticOutputParser(pydantic_object=QueryResponse)

    system_prompt = """Tu es un assistant de recherche qui doit générer des mots clés qui seront utilisés dans un moteur de recherche. 
    Fais en sorte que ces mots clés représentent au mieux ce qui serait nécessaire à la recherche. 
    Donne uniquement les mots clés et rien d'autre en anglais. Génère exactement 5 mots clés et une catégorie principale.

    Format de réponse requis :
    {format_instructions}"""

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", "{input}")
    ])

    model = ChatOpenAI(
        api_key="lm-studio",
        base_url="http://localhost:1234/v1",
        model=models,
        temperature=0.7,
        max_tokens=4096
    )

    chain = prompt | model | parser


    try:
        response = chain.invoke({
            "input": question,
            "format_instructions": parser.get_format_instructions()
        })
        return response
    
    except Exception as e:
        print(f"Erreur de parsing : {e}")
        return None

def clean_output(output: str):
    response = re.sub(r'<thought>.*?</thought>', '', output)
    return response


def benchmark(question: str):
    models_list = get_model()
    models_list.remove("text-embedding-nomic-embed-text-v1.5")

    #models_list = ["granite-3.2-8b-instruct"]

    attempts = 10

    for model in models_list:
        results = []
        print(f"Modèle : {model}")
        time_response = []
        time_moy = []
        score = 0
        score_categorie = 0
        chargement_model = time.time()
        for i in range(attempts):
            print_1 = time.time()
            print(f"\nRéponse {i+1}:")
            result = get_structured_response(question,model)
            print(result)
            result = clean_output(result)
            reponse_time = time.time()
            if i == 0:
                time_response.append({"chargement_model": reponse_time - chargement_model })

            if result:
                if (result.querys and result.categories) is not None:
                    score += 1
                    print(f"Mots-clés : {result.querys}")
                    print(f"Catégorie : {result.categories}")
                
                if isinstance(result.categories, str):
                    score_categorie += 1
                elif isinstance(result.categories, list):
                    if len(result.categories) == 1:                        
                        score_categorie += 1

                results.append(result)
            
            time_moy.append(reponse_time - print_1)
            time_response.append({"reponse_time_" + str(i): reponse_time - print_1})

        end_time = time.time()
        time_response.append({"avg_reponse_time": sum(time_moy) / len(time_moy)})
        time_response.append({"total_time": end_time - chargement_model})
        scores = []
        scores.append(score/attempts)
        scores.append(score_categorie/attempts)
        
        print(f"Score : {score/attempts} Score_categorie : {score_categorie/attempts}")
        add_json("benchmark_output_parser.json",model, attempts, scores, time_response, results)
        


if __name__ == "__main__":
    question = "Pourquoi n'utilise t'on pas les réseaux de neurones convolutifs pour les LLMs ?"
    
    print(benchmark(question))