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


router = APIRouter(prefix="/bdd")

# Init classe base de donné 
bdd = Bdd()
graph_bdd = BDD_Node()



class AjoutRechercheEspace(BaseModel):
    subject: str
    objectif: str
    couleur : str 

@router.post("/CreeEspaceRecherche/")
async def CreeEspaceRecherche(EspaceRecherche: AjoutRechercheEspace):
    try:
        BDDEspace = RechercheEspace.create(EspaceRecherche.subject, EspaceRecherche.objectif, bdd)
        NodeBDDEspace = EspaceRechercheNode(graph_bdd,BDDEspace.id,BDDEspace.subject, BDDEspace.objectif,EspaceRecherche.couleur)
    
    except Exception as e:
        print("Erreur lors de la création d'un espace :", e)
        raise HTTPException(status_code=500, detail=str(e))

class SupprimerEspaceRechercheBody(BaseModel):
    id_espace: int

@router.post("/SupprimerEspaceRecherche/")
async def SupprimerEspaceRecherche(body: SupprimerEspaceRechercheBody):
    try:
        id_espace = body.id_espace
        BDDEspace = RechercheEspace.load(id_espace, bdd)
        NodeBDDEspace = EspaceRechercheNode.load(graph_bdd, id_espace)

        boolsupprBDD = BDDEspace.supprimer()
        # Optionnel : suppression du noeud dans Neo4j
        # boolsupprNodeBDD = NodeBDDEspace.supprimer()

        return {"espace": boolsupprBDD}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/GetEspaceRecherche/")
async def getGetEspaceRecherche(id: str):
    try:
        BDDEspace = RechercheEspace.load(id, bdd)
        NodeBDDEspace = EspaceRechercheNode.load(graph_bdd, id)

        # On retourne bien des dictionnaires
        return {
            "espace": BDDEspace.dico() if BDDEspace else None,
            "node": NodeBDDEspace.dico() if NodeBDDEspace else None
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    
@router.get("/GetEspaceRecherches/")
async def GetEspaceRecherches():
    try:
        ListEspaces = bdd.get_EspaceRecherches()
        return [espace.dico() for espace in ListEspaces]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.get("/GetRecherches/")
async def GetRecherches(id_Espaces_Recherches: int):
    try:
        ListRecherches = bdd.get_Recherches(id_Espaces_Recherches)
        return [rech.dico() for rech in ListRecherches]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



