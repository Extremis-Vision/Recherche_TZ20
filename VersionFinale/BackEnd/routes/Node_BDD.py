import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from fastapi import APIRouter, HTTPException
from typing import List,Optional
from pydantic import BaseModel
from BDD.RechercheEspace import RechercheEspace

from BDD.BDD import Bdd
from fastapi.responses import StreamingResponse
from Node_BDD.graph import BDD_Node
from Node_BDD.EspaceRecherchNode import EspaceRechercheNode


router = APIRouter(prefix="/nodebdd")


graph_bdd = BDD_Node()

@router.get("/GetAllNode/")
async def GetAllNode():
    try:
        return graph_bdd.parse_graph_neo4j()    
    except Exception as e:
        print("Erreur lors de la création d'un espace :", e)
        raise HTTPException(status_code=500, detail=str(e))