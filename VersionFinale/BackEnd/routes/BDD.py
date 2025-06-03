import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from fastapi import APIRouter, HTTPException
from typing import List,Optional
from pydantic import BaseModel
from BDD.RechercheEspace import RechercheEspace
from BDD.BDD import Bdd
from fastapi.responses import StreamingResponse
from Node_BDD.graph import GraphDatabase
from Node_BDD.EspaceRecherchNode import EspaceRechercheNode


router = APIRouter(prefix="/bdd")

# Init classe base de donné 
bdd = Bdd()
graph_bdd = GraphDatabase()



class AjoutRechercheEspace(BaseModel):
    subject: str
    objectif: str
    couleur : str 

@router.get("/CreeEspaceRecherche/")
async def CreeEspaceRecherche(EspaceRecherche: AjoutRechercheEspace):
    try:
        BDDEspace = RechercheEspace.create(EspaceRecherche.subject, EspaceRecherche.objectif, bdd)
        NodeBDDEspace = EspaceRechercheNode(graph_bdd,BDDEspace.id,BDDEspace.subject, BDDEspace.objectif,EspaceRecherche.couleur)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/GetEspaceRecherche/")
async def getGetEspaceRecherche(id : str):
    try:
        BDDEspace = RechercheEspace.load(id, bdd)
        NodeBDDEspace = EspaceRechercheNode.load(graph_bdd,id)

        return BDDEspace.dico(),NodeBDDEspace.dico()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/GetEspaceRecherches/")
async def GetEspaceRecherches():
    try:
        ListEspaces = bdd.get_EspaceRecherche()

        return ListEspaces

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    



