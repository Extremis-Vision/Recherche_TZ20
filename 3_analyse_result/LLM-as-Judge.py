from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import requests
from typing import Dict, Any
from langchain_openai import ChatOpenAI


# 1. Configuration du template
eval_template = """[SYSTEM]
Vous êtes un expert en évaluation de LLM. Analysez cette réponse:

[SYSTEM PROMPT]
{system_prompt}

[QUESTION]
{question}

[RÉPONSE]
{reponse}

[CRITÈRES]
1. Pertinence technique (0-3)
2. Exhaustivité des concepts (0-3) 
3. Précision terminologique (0-2)
4. Originalité des insights (0-2)

[FORMAT DE SORTIE]
{{"score_total": 0-10, "critères": [...]}}"""

prompt = ChatPromptTemplate.from_template(eval_template)

parser = JsonOutputParser()

def evaluate_with_langchain():
    model = ChatOpenAI(
        api_key="lm-studio",
        base_url="http://localhost:1234/v1",
        model="deepseek-r1-distill-qwen-7b",
        temperature=0.7,
        max_tokens=4096
    )    
    
    chain = prompt | model | parser
    
    result = chain.invoke({
        "system_prompt": """Tu es un assistant de recherche qui doit 
                générer des mots clées qui seront utilisé dans un moteur de recherche 
                fait en sorte que ses mots clées représente au mieux ce qui serait necessaire 
                à la recherche. Donne moi uniquement les mots clées et rien d'autre en anglais,
                tu dois en générer  mots clées et une catégorie. Ta réponse doit être structuré de la manière suivante : 
                {"querys": ["mot1", "mot2", "mot3", "mot4", "mot5"],"categories":"catégorie"}, 
                ne mets absolument aucune pas de balyse : ```json  """,
        "question": "Pourquoi n'utilise t'on pas les réseaux de neurones convulatif pour les llms ?",
        "reponse": "{'mot_cle': ['convolutional neural networks', 'LLMs', 'recurrent neural networks', 'long short-term memory', 'CNN vs RNN'], 'categories': 'machine learning'}"
    })
    
    return result


print(evaluate_with_langchain ())
