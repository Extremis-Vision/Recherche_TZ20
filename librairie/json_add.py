import json 
import os

def add_json(file_name,model,attempts, score, time_response, results):
    try:    
        with open(file_name, 'r') as file:
            data = json.load(file)

    except FileNotFoundError:
        data = {}

    if 'results' not in data:
        data['results'] = []

    new_result = {
        "model_name": model,
        "temperature": 0.7,
        "max_tokens": 4096,
        "attempts": attempts,
        "time": time_response,
        "score": score,
        "result": str(results)
    }

    data['results'].append(new_result)

    with open(file_name, 'w') as file:
        json.dump(data, file, indent=4)

    print("Résultat ajouté au fichier JSON.")