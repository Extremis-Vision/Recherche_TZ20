import requests

AIURL = "http://192.168.0.18:1234/v1"

def ask_ai(system_prompt,prompt,model, temperatuere=0.7, tokens=4096):
    headers = {
    "Content-Type": "application/json"
    }

    payload = {
    "model": model,  # Remplacez par le nom du mod�le charg�
    "messages": [
        {"role": "system", "content": system_prompt
         },
        {"role": "user", "content": prompt}
    ],
    "temperature": temperatuere,
    "max_tokens": tokens
    }

    response = requests.post(AIURL+"/chat/completions", json=payload, headers=headers)
    if response.status_code == 200:
        assistant_reply = response.json()["choices"][0]["message"]["content"]
        return assistant_reply
    else:
        print(f"Erreur : {response.status_code}, {response.text}")

def get_models():
    headers = {
    "Content-Type": "application/json"
    }

    response = requests.get(AIURL+"/models")
    if response.status_code == 200:
        data = response.json()['data']
    else:
        print(f"Erreur : {response.status_code}, {response.text}")
        return []
    models = []
    for i in data:
        if isinstance(i["id"],str):
            models.append(i['id'])
    return models