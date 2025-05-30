from pydantic import BaseModel, Field
from typing import List, Dict, Any

def keywords_model(numberKeyWord: int = 5):
    class KeyWords(BaseModel):
        questions: List[str] = Field(
            description=f"Provide a list of {numberKeyWord} keywords or key sentences for research."
        )
        language: str = Field(
            description="Give the language of the user prompt in full letter"
        )
        categorie: str = Field(
            description="Give the categorie/ domain of the question"
        )
        boolean: str = Field(
            description="Can the information demanded be given by a specific function respond true if (function : get a price, get the weather), false if not."
        )
    return KeyWords