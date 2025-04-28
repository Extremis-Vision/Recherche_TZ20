from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from typing import List
import csv
import os
import time 

def get_structured_response(question: str, models : str):
    class QueryResponse(BaseModel):
        querys: List[str] = Field(description="Liste de 5 mots-clés de recherche en anglais")
        categories: str = Field(description="Catégorie principale de la recherche")

    # Étape 2: Initialiser le parser
    parser = PydanticOutputParser(pydantic_object=QueryResponse)

    system_prompt = """Tu es un assistant de recherche qui doit générer des mots clés qui seront utilisés dans un moteur de recherche. 
    Fais en sorte que ces mots clés représentent au mieux ce qui serait nécessaire à la recherche. 
    Donne uniquement les mots clés et rien d'autre en anglais. Génère exactement 5 mots clés.

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



def benchmark(question: str):
    score = 0
    results = []

    models_list = ["granite-3.2-8b-instruct","gemma-3-12b-it","mathstral-7b-v0.1","ministral-8b-instruct-2410","gemma-3-4b-it","qwq-lcot-7b-instruct"]
    #models_list = ["gemma-3-12b-it"]

    attempts = 10

    for model in models_list:
        print(f"Modèle : {model}")
        time_response = []
        chargement_model = time.time()
        time_response.append({"chargement_model": chargement_model})
        for i in range(attempts):
            print_1 = time.time()
            print(f"\nRéponse {i+1}:")
            result = get_structured_response(question,model)
            reponse_time = time.time()

            if result:
                if (result.querys and result.categories) is not None:
                    score += 1
                    print(f"Mots-clés : {result.querys}")
                    print(f"Catégorie : {result.categories}")
                results.append(result)
            
            time_response.append({"premier_print" : print_1 ,"reponse_time": reponse_time})
        
        end_time = time.time()
        time_response.append({"end_time": end_time})
        elapsed_time = end_time - chargement_model

        print("Temps écoulé : ", elapsed_time)


        print(f"Score : {score}")
        fieldnames = ['model_name', "attempts", 'score',"time" , "result"]

        file_exists = os.path.isfile('benchmark.csv')

        with open('benchmark.csv', 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            if not file_exists:
                writer.writeheader()
            
            writer.writerow({
                'model_name': model,
                "attempts": attempts,
                'score': score,
                "time": time_response,
                "result": str(results)
            })

        print("Results appended to benchmark.csv")


if __name__ == "__main__":
    question = "Pourquoi n'utilise t'on pas les réseaux de neurones convolutifs pour les LLMs ?"
    
    print(benchmark(question))