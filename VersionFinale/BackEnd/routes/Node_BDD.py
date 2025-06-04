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
from Node_BDD.relation import Relation
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
    try:
        noeud_current = Noeud.load(graph_bdd, node.id)
        if noeud_current is None:
            raise HTTPException(status_code=404, detail="Noeud non trouvé")
        return noeud_current.supprimer(graph_bdd)
    except Exception as e:
        print("Erreur lors de la suppression d'un noeud :", e)
        raise HTTPException(status_code=500, detail=str(e))


class CreationRelation(BaseModel):
    id_source: str
    id_target: str
    type: str
    description : str

@router.post("/CreeRelation/")
async def CreeRelation(creationrelationcurrent: CreationRelation):
    try:
        relation_current = Relation(
            source_id=creationrelationcurrent.id_source, 
            target_id=creationrelationcurrent.id_target, 
            type=creationrelationcurrent.type,
            description=creationrelationcurrent.description
        )
        relation_current.create(graph_bdd)
        return {"status": "success"}  
    except Exception as e:
        print("Erreur lors de la création d'une relation :", e)  
        raise HTTPException(status_code=500, detail=str(e))
    



class CreeNoeud(BaseModel):
    nom: str
    description: Optional[str] = None
    couleur: Optional[str] = None
    backgroundcolor: Optional[str] = None

@router.post("/CreeNoeud/")
async def CreeNoeud(creenoedcurrent: CreeNoeud):
    try:
        noeud_current = Noeud(
            nom=creenoedcurrent.nom,
            description=creenoedcurrent.description,
            couleur=creenoedcurrent.couleur,
        )
        noeud_current.cree(graph_bdd)
        return noeud_current
    except Exception as e:
        print("Erreur lors de la création d'un noeud :", e)
        raise HTTPException(status_code=500, detail=str(e))
