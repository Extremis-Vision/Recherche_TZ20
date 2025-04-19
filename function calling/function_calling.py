import requests
import json
import os
import time
from outils.weather import weather
from outils.ai import call_llm
from outils.scientist import maths


def rephrasal(prompt):
    rephrasal_assistant = "Tu es un assistant fonctionnel qui réécrit les données donnée en entrer pour les adpatés à l'oral et les renvoyer. Garde un niveau de précision dans tes réponses par rapport à ce qui t'es donner en input"
    return call_llm(rephrasal_assistant, prompt)

def ask_ai(prompt):
    function_calling_assistant = "Tu as accès a plusieurs type et possibilité de function et tu dois demandé celle qui t's nécessaire pour cela tu renvois un json comme suivant {'function_call': {'name': 'function_name', 'arguments': {'arg1': 'value1', ... }}} et tu dois faire en sorte que le nom de la fonction soit le plus explicite possible et que les arguments soient les plus pertinents possibles. En sachant que tu as accès au fonction : stockexchange_price(), stockexchange_price_history(timeframe), cryptoprice, cryptoprice_history(timeframe), search_query(query, engines=None, categories=None),weather(location = None si n'est pas précisé tu ne donne aucun arguments) Mettre une location uniquement si précisé, agenda(), ['math','physics','mecanics','info'] #Utile pour toutes questions des domaines indiqué permet de résoudre ou de répondre au problème mets en arguments ce qui est demandé, homeassistant(),  . Tu ne renvoie que le json rien d'autre. Tu peux mettre plusieurs fonctions dans function_call"
    return call_llm(function_calling_assistant, prompt)


if __name__ == "__main__":
    #prompt = str(input("qu'est ce que vous voulez demandez à l'agent : ")) #exemple de question : "Qu'est ce que tu me conseil de porter ?"
    prompt = "Est ce que c'est un temps pour faire de la boxe thai "
    response = ask_ai(prompt)
    response = response.strip()
    response = response.replace("```", "")
    response = response.replace("json", "")
    response = response.replace("```", "")
    response = response.replace("\n", "") 

    try:
        # Parse JSON response
        json_data = json.loads(response)
        
        # Get the first function call
        if json_data["function_call"] and len(json_data["function_call"]) > 0:
            first_function = json_data["function_call"][0]
            commande = first_function["name"]
            arguments = first_function.get("arguments", {})  # Using get() with default empty dict
                        
            print(f"Executing function: {commande}")
            
            # Check if function exists and call it with arguments
            if commande in globals():
                if arguments:  # If arguments is not empty
                    temp = globals()[commande](**arguments)
                else:
                    temp = globals()[commande]()
                print(rephrasal(temp + " \n" + prompt))
            else:
                print(f"Function {commande} not found")
                
        # Execute second function if needed
        if len(json_data["function_call"]) > 1:
            second_function = json_data["function_call"][1]
            commande = second_function["name"]
            arguments = second_function.get("arguments", {})  # Using get() with default empty dict
            
            if commande in globals():
                if arguments:  # If arguments is not empty
                    temp = globals()[commande](**arguments)
                else:
                    temp = globals()[commande]()
                print(rephrasal(temp + " \n" + prompt))
                    
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
    except KeyError as e:
        print(f"Error accessing JSON key: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
