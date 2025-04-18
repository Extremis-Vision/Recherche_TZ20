import requests
import json
import os
import time

AIURL = "http://localhost:1234/v1/chat/completions"

def ask_ai(prompt):
    headers = {
    "Content-Type": "application/json"
    }

    payload = {
    "model": "gemma-3-12b-it",  # Remplacez par le nom du mod�le charg�
    "messages": [
        {"role": "system", "content": "Tu as accès a plusieurs type et possibilité de function et tu dois demandé celle qui t's nécessaire pour cela tu renvois un json comme suivant {'function_call': {'name': 'function_name', 'arguments': {'arg1': 'value1', ... }}} et tu dois faire en sorte que le nom de la fonction soit le plus explicite possible et que les arguments soient les plus pertinents possibles. En sachant que tu as accès au fonction : stockexchange_price(), stockexchange_price_history(timeframe), cryptoprice, cryptoprice_history(timeframe), search_query(query, engines=None, categories=None),weather(location=None) Mettre une location uniquement si précisé, agenda(), scientist('['math','physics','mecanics','info']') #Utile pour toutes questions des domaines indiqué permet de résoudre ou de répondre au problème, homeassistant(),  . Tu ne renvoie que le json rien d'autre. Tu peux mettre plusieurs fonctions dans function_call"},
        {"role": "user", "content": prompt}
    ],
    "temperature": 0.7,
    "max_tokens": 4096
    }

    response = requests.post(AIURL, json=payload, headers=headers)
    if response.status_code == 200:
        assistant_reply = response.json()["choices"][0]["message"]["content"]
        print(f"{assistant_reply}")
    else:
        print(f"Erreur : {response.status_code}, {response.text}")


if __name__ == "__main__":
    for i in range(5):
        print("Réponse : ",i+1)
        ask_ai("explique le polymotphism et le dynamic binding en java")

