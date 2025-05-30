from pydantic import BaseModel, Field
from typing import List

class KeyWords(BaseModel):
    questions: List[str] = Field(description="List of keywords or key sentences for research.")
    language: str = Field(description="Language of the user prompt.")
    categorie: str = Field(description="Category/domain of the question.")
    boolean: str = Field(description="Can the information be given by a specific function?")