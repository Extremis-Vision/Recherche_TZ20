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
            f"Your main objective is to return a set of precise keywords to perform a web search for the given question. Only generate keywords that are highly specific to the domain, such as proper nouns, names of tools, companies, organizations, or other unique terms directly relevant to the question.\n"
            f"Do not generate general or broad keywords—focus only on unique, domain-specific terms, including names the model may not know but are essential for targeted search.\n"
            f"Your response must be strictly in JSON format.\n"
            f"You must generate exactly {numberKeyWord} keywords, always in English.\n"
            f"\n"
            f"INSTRUCTIONS:\n"
            f"- Respond with a single JSON object only—no extra text, comments, or explanations.\n"
            f"- The JSON object must include:\n"
            f"    - 'questions': a list of exactly {numberKeyWord} specific English keywords (proper nouns, tool names, company names, etc.), but allso precise query to have a good context.\n"
            f"    - 'categorie': the main category or domain of the question (e.g., 'technology', 'health').\n"
            f"    - 'boolean': 'true' if a specific function (such as price lookup or weather) can provide the answer; otherwise, 'false'.\n"
            f"\n"
            f"EXAMPLE OUTPUT FORMAT (for 2 keywords):\n"
            f'{{{{"questions": ["OpenAI", "ChatGPT"], "categorie": "technology", "boolean": "false"}}}}\n'
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
            return [response.questions,response.categorie,response.boolean]
        except Exception as e:
            print(f"Erreur lors de la récupération des mots-clés : {e}")
            return None
        

# Exemple utilisation 
#search = SimpleSearch()
#print(search.get_key_word_search("Qu'est ce que l'ia "))
