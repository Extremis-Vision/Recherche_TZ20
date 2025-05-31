import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from fastapi import APIRouter, HTTPException
from typing import List,Optional
from pydantic import BaseModel
from Recherche.SimpleSearch import SimpleSearch
from Recherche.RechercheBasique import RechercheBasique
from Generation.ChromaDB import ChromaDB

router = APIRouter(prefix="/recherche")

class RechercheRequest(BaseModel):
    recherche: str
    numberKeyWord: int = 5
    model_name: Optional[str] = None

@router.post("/keywords/")
async def get_keywords(recherche: RechercheRequest):
    """
    Retourne une liste de mots-clés pour une recherche donnée.
    """
    try:
        search = SimpleSearch(model_name=recherche.model_name)
        result = search.get_key_word_search(recherche.recherche, recherche.numberKeyWord)
        print(result)
        if result is None:
            raise HTTPException(status_code=400, detail="Erreur lors de la génération des mots-clés")
        questions, categorie, boolean = result
        return {
            "questions": questions,
            "categorie": categorie,
            "boolean": boolean
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/SimpleSearch")
async def get_keywords(MotCLee: List[str]):
    """
    Retourne la réponse de la recherche avec les mots clées
    """
    try:
