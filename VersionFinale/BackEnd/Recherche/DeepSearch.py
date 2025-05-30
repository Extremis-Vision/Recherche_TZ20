import sys, os 

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Generation.model_provider import get_model
from Recherche.RechercheBasique import RechercheBasique
from Recherche.Keywords import keywords_deepsearch
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from typing import List, Optional


class DeepSearch:
    def get_key_word_deepsearch(recherche: str, NB_MotClee_Sujet: int = 3, NB_MotClee_Specifique : int = 2, models: str = "ministral-8b-instruct-2410") -> Optional[List[str]]:

        parser = PydanticOutputParser(pydantic_object=keywords_deepsearch(NB_MotClee_Sujet,NB_MotClee_Specifique))
        # Échappe les accolades pour LangChain
        format_instructions = parser.get_format_instructions().replace("{", "{{").replace("}", "}}")

        system_prompt = (
            f"You are an assistant for web search research.\n"
            f"Given a question, return a JSON object with two keys:\n"
            f"- 'KeywordSubjectDef': a list of {NB_MotClee_Sujet} broad keywords or key subjects for a wide domain search, but only on what demanded in the question.\n"
            f"- 'SpecificKeyWord': a list of {NB_MotClee_Specifique} more specific keywords or key sentences for detailed research that will help answer the question when searching the internet.\n"
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