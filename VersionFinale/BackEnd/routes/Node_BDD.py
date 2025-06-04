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
from Node_BDD.noeud import Noeud
from Node_BDD.EspaceRecherchNode import EspaceRechercheNode
from pydantic import BaseModel


router = APIRouter(prefix="/nodebdd")


graph_bdd = BDD_Node()

@router.get("/GetAllNode/")
async def GetAllNode():
    try:
        graph_dico = graph_bdd.parse_graph_neo4j() 
        return graph_dico   
    except Exception as e:
        print("Erreur lors de la création d'un espace :", e)
        raise HTTPException(status_code=500, detail=str(e))
    

class NodeId(BaseModel):
    id: str

@router.post("/SupprimerNode/")
async def SupprimerNode(node: NodeId):
    print("Reçu :", node)
    try:
        noeud_current = Noeud.load(graph_bdd, node.id)
        print("Noeud chargé :", noeud_current.dico())
        return noeud_current.supprimer(graph_bdd)
    except Exception as e:
        print("Erreur lors de la suppression d'un noeud :", e)
        raise HTTPException(status_code=500, detail=str(e))

