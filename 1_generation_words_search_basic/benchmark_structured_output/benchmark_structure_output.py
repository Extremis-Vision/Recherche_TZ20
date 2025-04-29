import requests
import json
import os
import time
import csv
import sys

AIURL = "http://192.168.0.18:1234/v1/chat/completions"

def ask_ai(prompt,model):
    headers = {
    "Content-Type": "application/json"
    }

    payload = {
    "model": model,  # Remplacez par le nom du mod�le charg�
    "messages": [
        {"role": "system", "content": "Tu es un assistant de recherche qui doit générer des mots clées qui seront utilisé dans un moteur de recherche fait en sorte que ses mots clées représente au mieux ce qui serait necessaire à la recherche. Donne moi uniquement les mots clées et rien d'autre en anglais, tu dois en générer 5. Ta réponse doit être structuré de la manière suivante : {'querys': ['mot1', 'mot2', 'mot3', 'mot4', 'mot5'],'categories':'catégorie'}, ne mets absolument aucune pas de balyse : ```json  "},
        {"role": "user", "content": prompt}
    ],
    "temperature": 0.7,
    "max_tokens": 4096
    }

    response = requests.post(AIURL, json=payload, headers=headers)
    if response.status_code == 200:
        assistant_reply = response.json()["choices"][0]["message"]["content"]
        return assistant_reply
    else:
        print(f"Erreur : {response.status_code}, {response.text}")

def add_csv(model,attempts, score, time_response, results): 
    fieldnames = ['model_name', "attempts", 'score',"time" , "result"]

    file_exists = os.path.isfile('benchmark.csv')

    with open('benchmark_structured_output.csv', 'a', newline='', encoding='utf-8') as csvfile:
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

    print("Ajout au CSV terminé.")


def benchmark(question: str):
    results = []

    #models_list = ["granite-3.2-8b-instruct","gemma-3-12b-it","mathstral-7b-v0.1","ministral-8b-instruct-2410","gemma-3-4b-it","qwq-lcot-7b-instruct"]
    models_list = ["gemma-3-12b-it"]

    attempts = 10

    for model in models_list:
        score = 0
        time_moy = []
        print(f"Modèle : {model}")
        time_response = []
        chargement_model = time.time()
        for i in range(attempts):
            print_1 = time.time()
            print(f"\nRéponse {i+1}:")
            response = ask_ai(question,model)
            reponse_time = time.time()
            time_response.append({"chargement_model": reponse_time - chargement_model })

            try:
                #Traitement de la réponse
                response = response.strip()
                response = response.replace("```", "")
                response = response.replace("json", "")
                response = response.replace("```", "")
                response = response.replace("\n", "") 
                response_final = json.loads(response)
                if "querys"  in response_final or "categories" in response_final:
                    results.append({"mot_cle" : response_final["querys"], "categories": response_final["categories"]})
                    print("Mots clées : ",response_final["querys"],response_final["categories"])
                    score += 1
                time_moy.append(reponse_time - print_1)
                time_response.append({"reponse_time_" + str(i): reponse_time - print_1})
            except json.JSONDecodeError as e:
                response_final = "Erreur de décodage JSON : " + str(e)
                continue

            except Exception as e:
                response_final = "Erreur : " + str(e)
                continue
                
        end_time = time.time()
        end_time = time.time()
        time_response.append({"avg_reponse_time": sum(time_moy) / len(time_moy)})
        time_response.append({"total_time": end_time - chargement_model})
        print(f"Score : {score}")

        add_csv(model, attempts, score, time_response, results)


if __name__ == "__main__":
    benchmark("Pourquoi n'utilise t'on pas les réseaux de neurones convulatif pour les llms ?")
        
