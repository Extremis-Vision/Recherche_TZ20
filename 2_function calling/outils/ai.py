import requests
import json

def call_llm(system_prompt, user_prompt, temperature=0.7, max_tokens=4096, model="gemma-3-12b-it"):
    """
    Call the LLM with the given prompt and return the response.
    """

    AIURL = "http://localhost:1234/v1/chat/completions"


    headers = {
    "Content-Type": "application/json"
    }

    payload = {
    "model": model,
    "messages": [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ],
    "temperature": temperature,
    "max_tokens": max_tokens
    }

    response = requests.post(AIURL, json=payload, headers=headers)
    if response.status_code == 200:
        assistant_reply = response.json()["choices"][0]["message"]["content"]
        return assistant_reply
    else:
        print(f"Erreur : {response.status_code}, {response.text}")