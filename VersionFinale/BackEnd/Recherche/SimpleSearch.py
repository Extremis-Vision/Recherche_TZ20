import sys, os 

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Recherche.RechercheBasique import RechercheBasique
from Recherche.Keywords import keywords_simplesearch
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from typing import List, Optional
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

chemin_env = os.path.join(os.path.dirname(__file__), '..', '..', '.env')

load_dotenv(chemin_env)

class SimpleSearch(RechercheBasique):
    def __init__(self,  model_name : str = None, engines : str = None):
        super().__init__(engines)
        if model_name == None:
            self.model_name = "ministral-8b-instruct-2410"
        else :
            self.model_name = model_name
        self.api_key = os.getenv("AI_API_KEY", "lm-studio")
        self.base_url = os.getenv("AI_URL", "http://localhost:1234/v1")

    def _get_model(self):
            return ChatOpenAI(
                api_key=self.api_key,
                base_url=self.base_url,
                model=self.model_name,
                temperature=0.7,
                max_tokens=4096,
                streaming=True
            )

    def get_key_word_search(self,recherche: str, numberKeyWord: int = 5, models: str = "ministral-8b-instruct-2410") -> Optional[List[str]]:
        parser = PydanticOutputParser(pydantic_object=keywords_simplesearch(numberKeyWord))
        # Échappe les accolades pour LangChain
        format_instructions = parser.get_format_instructions().replace("{", "{{").replace("}", "}}")

        system_prompt = (
            f"Your main objective is to return a set of keywords or key sentences to perform a web search, your response must be only and only in the JSON format.\n"
            f"You must generate exactly {numberKeyWord} keywords or key sentences that are precise and directly relevant to the user's question.\n"
            f"\n"
            f"IMPORTANT INSTRUCTIONS:\n"
            f"- Your response MUST be a single JSON object, with no extra text, comments, or explanations.\n"
            f"- The JSON object must contain the following fields:\n"
            f"    - 'questions': a list of exactly {numberKeyWord} keywords or key sentences, the keywords must always be in English.\n"
            f"    - 'categorie': the category or domain of the question (e.g., 'technology', 'health').\n"
            f"    - 'boolean': 'true' if the information requested can be provided by a specific function (such as getting a price or the weather), otherwise 'false'.\n"
            f"\n"
            f"EXAMPLE OUTPUT FORMAT (for 2 keywords):\n"
            f'{{{{"questions": ["keyword1", "keyword2"], "language": "language", "categorie": "technology", "boolean": "false"}}}}\n'
            f"\n"
            f"Do not add any explanations or text outside this JSON format.\n"
            f"\n"
            f"{format_instructions}\n"
        )


        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", "{input}")
        ])

        chain = prompt | self._get_model() | parser

        try:
            response = chain.invoke({
            "input": recherche
            })
            return [response.questions,response.language,response.categorie,response.boolean]
        except Exception as e:
            print(f"Erreur lors de la récupération des mots-clés : {e}")
            return None
        

# Exemple utilisation 
# print(SimpleSearch.get_key_word_search("Qu'est ce que l'ia "))