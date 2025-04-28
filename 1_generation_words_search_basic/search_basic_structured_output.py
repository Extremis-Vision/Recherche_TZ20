import requests
import json
import os
import time

AIURL = "http://192.168.0.18:1234/v1/chat/completions"

def ask_ai(prompt):
    headers = {
    "Content-Type": "application/json"
    }

    payload = {
    "model": "gemma-3-12b-it",  # Remplacez par le nom du mod�le charg�
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
        print(f"{assistant_reply}")
    else:
        print(f"Erreur : {response.status_code}, {response.text}")


if __name__ == "__main__":
    for i in range(5):
        print("Réponse : ",i+1)
        ask_ai("Pourquoi n'utilise t'on pas les réseaux de neurones convulatif pour les llms ?")

