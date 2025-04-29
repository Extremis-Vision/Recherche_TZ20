import requests

AIURL = "http://192.168.0.18:1234/v1/chat/completions"

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

    response = requests.post(AIURL, json=payload, headers=headers)
    if response.status_code == 200:
        assistant_reply = response.json()["choices"][0]["message"]["content"]
        return assistant_reply
    else:
        print(f"Erreur : {response.status_code}, {response.text}")