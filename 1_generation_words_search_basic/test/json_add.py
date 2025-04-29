import json


def add_to_json(model,attempts, score, time_response, results):
    with open('data.json', 'r') as file:
        data = json.load(file)

    if 'results' not in data:
        data['results'] = []

    new_result = {
        "model_name": model,
        "temperature": 0.7,
        "max_tokens": 4096,
        "attempts": attempts,
        "score": score,
        "time": time_response,
        "result": str(results)
    }

    data['results'].append(new_result)

    with open('data.json', 'w') as file:
        json.dump(data, file, indent=4)
