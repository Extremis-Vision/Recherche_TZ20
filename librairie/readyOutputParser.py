from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from typing import List
from json_add import add_json
from ask_ai import get_model
import os
import time 
import re



def get_model(models : str):
    model = ChatOpenAI(
        api_key="lm-studio",
        base_url="http://localhost:1234/v1",
        model=models,
        temperature=0.7,
        max_tokens=4096
    )
    return model

def get_key_word(question: str, models : str):
    class QueryResponse(BaseModel):
        querys: List[str] = Field(description="Liste de 5 mots-clés de recherche en anglais")
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
        return response
    
    except Exception as e:
        print(f"Erreur de parsing : {e}")
        return None

def get_research_question(question: str, models : str):
    class QueryResponse(BaseModel):
        questions: List[str] = Field(description="give questions to sepecify the types of research and the type of data to be used")

    # Étape 2: Initialiser le parser
    parser = PydanticOutputParser(pydantic_object=QueryResponse)

    system_prompt = """You are an intelligent AI search assistant designed to help users find precise information based on their needs. Your primary goal is to ask a set of 3 to 5 clarifying questions to refine the user's search intent before providing tailored search results. 

**Instructions:**
1. **Engage the User:** Start by acknowledging the user's initial query in a friendly manner.
2. **Ask Clarifying Questions:** Generate 3 to 5 relevant questions that will help narrow down the user's intent. Ensure these questions cover different aspects of the topic.
3. **Dynamic Response Generation:** Adapt your questions based on the user's responses, ensuring to seek clarity on any ambiguous terms.
4. **Provide Tailored Search Results:** Once enough information is gathered, summarize the best options available based on the refined query.
5. **Encourage Interaction:** Maintain a conversational tone and encourage the user to elaborate on their needs if necessary.

**User Input Example:** 
"I need AI tools for marketing."

**Expected Output Example:**
1. "That's great! Could you specify what type of marketing tools you're looking for, such as social media marketing, email campaigns, or SEO?"
2. "Are you interested in free tools or are you open to paid options?"
3. "Is your focus on small businesses or larger enterprises?"

Once the user answers, summarize the information and provide a list of tailored tools or resources based on their specific requirements.
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
        return response
    
    except Exception as e:
        print(f"Erreur de parsing : {e}")
        return None



def clean_output(output: str):
    response = re.sub(r'<thought>.*?</thought>', '', output)
    return response



print(get_research_question("What is the impact of climate change on biodiversity?", "gemma-3-12b-it-qat"))