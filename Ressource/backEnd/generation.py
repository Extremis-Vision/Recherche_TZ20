from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from typing import List, Optional
from dotenv import load_dotenv
import os
import lmstudio as lms

load_dotenv()
AIURL = os.getenv("AIURL")

def get_model(models: str):
    return ChatOpenAI(
        api_key="lm-studio",
        base_url=AIURL,
        model=models,
        temperature=0.7,
        max_tokens=4096,
        streaming=True
    )



def get_key_word_deepsearch(recherche: str, KeywordSubjectDef: int = 3, SpecificKeyWord : int = 2, models: str = "ministral-8b-instruct-2410") -> Optional[List[str]]:
    
    
    
    class Recherche(BaseModel):
        KeywordSubjectDef: List[str] = Field(
        description="A list of broad keywords or key subjects for wide domain search."
    )
        SpecificKeyWord: List[str] = Field(
        description="A list of more specific keywords or key sentences for detailed research."
    )

    parser = PydanticOutputParser(pydantic_object=Recherche)
    # Échappe les accolades pour LangChain
    format_instructions = parser.get_format_instructions().replace("{", "{{").replace("}", "}}")

    system_prompt = (
        f"You are an assistant for web search research.\n"
        f"Given a question, return a JSON object with two keys:\n"
        f"- 'KeywordSubjectDef': a list of {KeywordSubjectDef} broad keywords or key subjects for a wide domain search, but only on what demanded in the question.\n"
        f"- 'SpecificKeyWord': a list of {SpecificKeyWord} more specific keywords or key sentences for detailed research that will help answer the question when searching the internet.\n"
        "EXAMPLE OUTPUT:\n"
        '{{"KeywordSubjectDef": ["transformer architecture", "transformer", "deep learning"], '
        '"SpecificKeyWord": ["use of transformer ai", "where are transformers used", "latest advancement on transformer research"]}}'
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", "{input}")
    ])

    chain = prompt | get_model(models) | parser

    try:
        response = chain.invoke({
        "input": recherche
        })
        return {
            "KeywordSubjectDef": response.KeywordSubjectDef,
            "SpecificKeyWord": response.SpecificKeyWord
        }
    except Exception as e:
        print(f"Erreur lors de la récupération des mots-clés : {e}")
        return None

def get_key_word_search(recherche: str, numberKeyWord: int = 5, models: str = "ministral-8b-instruct-2410") -> Optional[List[str]]:
    class Recherche(BaseModel):
        questions: List[str] = Field(
            description=f"Provide a list of {numberKeyWord} keywords or key sentences for research. "
        )
        language: str = Field(
            description=f"Give the language of the user prompt in full letter"
        )
        categorie: str = Field(
            description=f"Give the categorie/ domain of the question"
        )
        boolean: str = Field(
            description=f"Can the information demanded be given by a specific function respond true if (function : get a price, get the weather)"
        )

    

    parser = PydanticOutputParser(pydantic_object=Recherche)
    # Échappe les accolades pour LangChain
    format_instructions = parser.get_format_instructions().replace("{", "{{").replace("}", "}}")

    system_prompt = (
    f"Your main objective is to return a set of keywords or key sentences to perform a web search. \n"
    f"Generate exactly {numberKeyWord} terms that will be used to answer the user's question. "
    f"Choose them carefully and make sure they are precise and relevant to the question.\n"
    f"EXAMPLE OUTPUT FORMAT (for 2 keywords):\n"
    f'{{{{"questions": ["keyword1", "keyword2"]}}}}\n'
    f"IMPORTANT: You must generate exactly {numberKeyWord} keywords or key sentences as instructed above, "
    f"and return them in the same JSON format as the example.\n"
    f"{format_instructions}\n"
)


    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", "{input}")
    ])

    chain = prompt | get_model(models) | parser

    try:
        response = chain.invoke({
        "input": recherche
        })
        return [response.questions,response.language,response.categorie,response.boolean]
    except Exception as e:
        print(f"Erreur lors de la récupération des mots-clés : {e}")
        return None
    


def response_with_context(prompt: str, context: str, model_name: str = "ministral-8b-instruct-2410", language : str = "French" ) -> Optional[str]:
    """
    Génère une réponse structurée à partir d'un prompt utilisateur et d'un contexte, en utilisant un output parser.
    """

    system_prompt = f"""
            You must generate a response using only the context provided below, and you must cite the sources of any information you use.
            Your response must be in the same language as the user's input here {language}.
            Citation format:
            At the end of each paragraph that uses information from a source, add the following citation format: (source_name)[link]

            Example:
            (datascientest.com)[https://datascientest.com/transformer-models-tout-savoir]

            Instructions:
            - Use only the provided context to answer the user's question.
            - Do not use any external information or sources.
            - For every factual statement or paragraph that uses information from the context, cite the relevant source in the specified format.
            - Write your response in the same language as the user's input here {language}.
            - Do not invent or hallucinate sources.
            - Only respond to the user query no more no less, but always source what you say in the user query language.
            - If your not capable to respond correctly just says what you lack of.

            Context to use:
            {context}
            """

    

    try:
        model = lms.llm(model_name)
        chat = lms.Chat(system_prompt)
        chat.add_user_message(prompt)

        prediction_stream = model.respond_stream(chat)

        print("Bot :", end=" ", flush=True)
        for fragment in prediction_stream:
            print(fragment.content, end="", flush=True)
        print()
        while True:
            user_input = input("Vous (laisser vide pour quitter) : ")
            if not user_input:
                break
            chat.add_user_message(user_input)

            # Lancement du streaming de la réponse
            prediction_stream = model.respond_stream(chat)

            print("Bot :", end=" ", flush=True)
            for fragment in prediction_stream:
                print(fragment.content, end="", flush=True)
            print()



    except Exception as e:
        print(f"Erreur lors de la génération de la réponse : {e}")
        return None
    

def response_deepsearch(prompt: str, context: str, model_name: str = "ministral-8b-instruct-2410") -> Optional[str]:
    """
    Génère une réponse structurée à partir d'un prompt utilisateur et d'un contexte, en utilisant un output parser.
    """

    class AnswerResponse(BaseModel):
        answer: str = Field(description="The answer to the user's question, citing sources as required.")

    parser = PydanticOutputParser(pydantic_object=AnswerResponse)
    format_instructions = parser.get_format_instructions().replace("{", "{{").replace("}", "}}")

    system_prompt = f"""
            You must generate a response using only the context provided below, and you must cite the sources of any information you use.
            Your response must be in the same language as the user's input.

            Citation format:
            At the end of each paragraph that uses information from a source, add the following citation format: (source_name)[link]

            Example:
            (datascientest.com)[https://datascientest.com/transformer-models-tout-savoir]

            Instructions:
            - Use only the provided context to answer the user's question.
            - Do not use any external information or sources.
            - For every factual statement or paragraph that uses information from the context, cite the relevant source in the specified format.
            - Write your response in the same language as the user's input.
            - Do not invent or hallucinate sources.
            - Only respond to the user query, but always source what you say.
            - Create a detail response explaining exaclty what the user want as respond, make to add emoji and a good presentation.

            Return your answer as a JSON object matching the following format:
            {format_instructions}

            Context to use:
            {context}
            """

    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", "{prompt}")
    ])

    chain = chat_prompt | get_model(model_name) | parser

    try:
        response = chain.invoke({
            "context": context,
            "prompt": prompt
        })
        # response is a Pydantic model instance, so access the answer attribute
        return response.answer

    except Exception as e:
        print(f"Erreur lors de la génération de la réponse : {e}")
        return None

