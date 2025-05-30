from pydantic import BaseModel, Field
from typing import List, Dict, Any

def keywords_simplesearch(NombreMotCle: int = 5):
    class KeyWords_SimpleSearch(BaseModel):
        questions: List[str] = Field(
            description=f"Provide a list of {NombreMotCle} keywords or key sentences for research."
        )
        categorie: str = Field(
            description="Give the categorie/ domain of the question"
        )
        boolean: str = Field(
            description="Can the information demanded be given by a specific function respond true if (function : get a price, get the weather), false if not."
        )
    return KeyWords_SimpleSearch


def keywords_deepsearch(NB_MotClee_Sujet: int = 3, NB_MotClee_Specifique : int = 2):
    class KeyWords_DeepSearch(BaseModel):
            MotClee_Sujet: List[str] = Field(
            description=f"A list of {NB_MotClee_Sujet} broad keywords or key subjects for wide domain search."
        )
            MotClee_Specifique: List[str] = Field(
            description=f"A list of {NB_MotClee_Specifique} more specific keywords or key sentences for detailed research."
        )
    return keywords_deepsearch