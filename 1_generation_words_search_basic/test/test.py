import requests

AIURL = "http://192.168.0.18:1234/v1/models"

def get_model():
    headers = {
    "Content-Type": "application/json"
    }

    response = requests.get(AIURL)
    data = response.json()['data']
    models = []
    for i in data:
        if isinstance(i["id"],str):
            models.append(i['id'])
    return models

print(get_model())
