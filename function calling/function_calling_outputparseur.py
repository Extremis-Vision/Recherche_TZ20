from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from typing import List
import csv
import os
from outils.weather import weather
from outils.ai import call_llm
from outils.scientist import maths


def get_function_calling_prompt( user_prompt: str, models = "gemma-3-12b-it"):
    # Étape 1: Définir la structure de sortie avec Pydantic
    class QueryResponse(BaseModel):
        querys: List[str] = Field(description="Données la bonne fonction à appeler et les arguments")

    # Étape 2: Initialiser le parser
    parser = PydanticOutputParser(pydantic_object=QueryResponse)

    # Étape 3: Créer le prompt avec instructions de formatage
    system_prompt = """Tu as accès a plusieurs type et possibilité de function et tu dois demandé celle qui t's nécessaire pour cela tu renvois un json comme suivant {'function_call': {'name': 'function_name', 'arguments': {'arg1': 'value1', ... }}} et tu dois faire en sorte que le nom de la fonction soit le plus explicite possible et que les arguments soient les plus pertinents possibles. En sachant que tu as accès au fonction : stockexchange_price(), stockexchange_price_history(timeframe), cryptoprice, cryptoprice_history(timeframe), search_query(query, engines=None, categories=None),weather(location = None si n'est pas précisé tu ne donne aucun arguments) Mettre une location uniquement si précisé, agenda(), ['math','physics','mecanics','info'] #Utile pour toutes questions des domaines indiqué permet de résoudre ou de répondre au problème mets en arguments ce qui est demandé, homeassistant(),  . Tu ne renvoie que le json rien d'autre. Tu peux mettre plusieurs fonctions dans function_call
    Tu dois renvoyer un json comme celui-ci : {'function_call': {'name': 'function_name', 'arguments': {'arg1': 'value1', ... }}} et tu dois faire en sorte que le nom de la fonction soit le plus explicite possible et que les arguments soient les plus pertinents possibles. En sachant que tu as accès au fonction : stockexchange_price(), stockexchange_price_history(timeframe), cryptoprice, cryptoprice_history(timeframe), search_query(query, engines=None, categories=None),weather(location = None si n'est pas précisé tu ne donne aucun arguments) Mettre une location uniquement si précisé, agenda(), ['math','physics','mecanics','info'] #Utile pour toutes questions des domaines indiqué permet de résoudre ou de répondre au problème mets en arguments ce qui est demandé, homeassistant(),  . Tu ne renvoie que le json rien d'autre. Tu peux mettre plusieurs fonctions dans function_call
    Format de réponse requis :
    {function_call: {name: function_name, arguments: {arg1: value1, ...}}}"""

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", "{user_prompt}"),
        ("assistant", "{function_call}"),
    ])



    model = ChatOpenAI(
    api_key="lm-studio",
    base_url="http://localhost:1234/v1",
    model=models,
    temperature=0.7,
    max_tokens=4096
    )

    # Étape 5: Créer la chaîne de traitement
    chain = prompt | model | parser

    try:
        response = chain.invoke({
                "input": user_prompt,
                "format_instructions": parser.get_format_instructions()
            })
        return response
    except Exception as e:
        print(f"Erreur de parsing : {e}")
        return None





def rephrasal(prompt):
    rephrasal_assistant = "Tu es un assistant fonctionnel qui réécrit les données donnée en entrer pour les adpatés à l'oral et les renvoyer. Garde un niveau de précision dans tes réponses par rapport à ce qui t'es donner en input"
    return call_llm(rephrasal_assistant, prompt)

print(get_function_calling_prompt("Est ce que c'est un temps pour faire de la boxe thai "))
