import requests
import json
import os
import time
import csv
import sys
from json_add import add_json
from ask_ai import ask_ai, get_model


AIURL = "http://192.168.0.18:1234/v1/chat/completions"

sys_prompt = """Generate 5 precise English search keywords and a category. Structure output as {"querys": ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"], "categories": "specific_category"}. Keywords must maximize search relevance. Exclude any formatting marks."""

def benchmark(question: str):
    results = []

    models_list = get_model()
    #models_list = ["granite-3.2-8b-instruct"]

    attempts = 10

    for model in models_list:
        score = 0
        score_categorie = 0
        time_moy = []
        print(f"Modèle : {model}")
        time_response = []
        chargement_model = time.time()
        for i in range(attempts):
            print_1 = time.time()
            response = ask_ai(sys_prompt, question, model)
            reponse_time = time.time()
            if i == 0:
                time_response.append({"chargement_model": reponse_time - chargement_model })


            #Traitement de la réponse
            response = response.strip()
            response = response.replace("```", "")
            response = response.replace("json", "")
            response = response.replace("```", "")
            response = response.replace("\n", "")

            try:
                response_final = json.loads(response)
                if "querys"  in response_final or "categories" in response_final:
                    results.append({"mot_cle" : response_final["querys"], "categories": response_final["categories"]})
                if isinstance(response_final['categories'], str):
                    score_categorie += 1
                elif isinstance(response_final['categories'], list):
                    if len(response_final['categories']) == 1:                        
                        score_categorie += 1
                
                score += 1

                time_moy.append(reponse_time - print_1)
                time_response.append({"reponse_time_" + str(i): reponse_time - print_1})

            except Exception as e:
                results.append({"Erreur" : str(e)})
                time_moy.append(reponse_time - print_1)
                time_response.append({"reponse_time_" + str(i): reponse_time - print_1})
                continue
                
        end_time = time.time()
        end_time = time.time()
        time_response.append({"avg_reponse_time": sum(time_moy) / len(time_moy)})
        time_response.append({"total_time": end_time - chargement_model})
        scores = []
        scores.append(score/attempts)
        scores.append(score_categorie/attempts)
        
        print(f"Score : {score/attempts} Score_categorie : {score_categorie/attempts}")
        add_json("benchmark_structured_output.json",model, attempts, scores, time_response, results)


if __name__ == "__main__":
    benchmark("Pourquoi n'utilise t'on pas les réseaux de neurones convulatif pour les llms ?")
        
