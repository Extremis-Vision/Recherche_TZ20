from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from typing import List
from json_add import add_json
from ask_ai import get_models
import os
import time 
import re
import sys
import json

def get_model(models : str):
    model = ChatOpenAI(
        api_key="lm-studio",
        base_url="http://localhost:1234/v1",
        model=models,
        temperature=0.7,
        max_tokens=4096
    )
    return model

def get_key_word(question: str, models : str = "gemma-3-12b-it-qat"):
    class QueryResponse(BaseModel):
        questions: List[str] = Field(description="Liste de 5 mots-clés de recherche en anglais")
        categories: str = Field(description="Catégorie principale de la recherche")

    # Étape 2: Initialiser le parser
    parser = PydanticOutputParser(pydantic_object=QueryResponse)

    system_prompt = """Tu es un assistant de recherche qui doit générer des mots clés qui seront utilisés dans un moteur de recherche. 
    Fais en sorte que ces mots clés représentent au mieux ce qui serait nécessaire à la recherche. 
    Donne uniquement les mots clés et rien d'autre en anglais. Génère exactement 5 mots clés et une catégorie principale.

    Format de réponse requis :
    {format_instructions}"""

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", "{input}")
    ])

    chain = prompt | get_model(models) | parser


    try:
        response = chain.invoke({
            "input": question,
            "format_instructions": parser.get_format_instructions()
        })
        return [response.questions, response.categories]
    
    except Exception as e:
        print(f"Erreur de parsing : {e}")
        return None

def get_research_question(question: str, models : str):
    class QueryResponse(BaseModel):
        questions: List[str] = Field(description="give questions to sepecify the types of research and the type of data to be used")

    # Étape 2: Initialiser le parser
    parser = PydanticOutputParser(pydantic_object=QueryResponse)

    system_prompt = """You are an intelligent AI search assistant designed to help users find precise information based on their needs. Your primary goal is to generate a set of 3 to 5 refined search suggestions or queries that anticipate and address the user's intent, rather than asking clarifying questions.

**Instructions:**
1. **Acknowledge the User:** Start by briefly recognizing the user's initial query in a friendly and engaging manner.
2. **Generate Search Suggestions:** Based on the user's input, provide 3 to 5 relevant and specific search queries or suggestions that reflect different possible directions or aspects related to their request.
3. **Adapt to User Feedback:** If the user selects or elaborates on a suggestion, further refine and expand the search options accordingly, ensuring the suggestions remain relevant and actionable.
4. **Summarize and Present Options:** Once the user's intent is clear, summarize the best search options or resources tailored to their refined needs.
5. **Encourage Exploration:** Maintain a conversational and positive tone, inviting the user to choose or further specify their preferences if needed.

**Note:** Do not ask clarifying questions. Only provide search suggestions or queries that help the user quickly find the information they are seeking.
"""

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", "{input}")
    ])

    chain = prompt | get_model(models) | parser


    try:
        response = chain.invoke({
            "input": question,
            "format_instructions": parser.get_format_instructions()
        })
        return response
    
    except Exception as e:
        print(f"Erreur de parsing : {e}")
        return None

def clean_output(output: str):
    response = re.sub(r'<thought>.*?</thought>', '', output)
    return response

def get_question(question: str, models : str):
    questions = get_research_question(question,models)
    if questions is None:
        return "Erreur lors de la génération de la question de recherche."
    questions = questions.questions
    for i in questions: 
        print(i)
    numberQuestion = int(input("Quels questions vous convients pour la recherche ?"))
    if numberQuestion > len(question):
        print("Donnez votre question pour la recherche :")
        question = str(input()) 
    else:
        question = questions[numberQuestion - 1]
    return question

def deep_search(prompt: str, models : str):
    question = get_question(prompt, models)
    prompt += question
    print(prompt)
    print(get_key_word(prompt, models))