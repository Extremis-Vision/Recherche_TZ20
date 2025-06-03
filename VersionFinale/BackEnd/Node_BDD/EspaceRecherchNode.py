import sys, os 

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Node_BDD.noeud import Noeud
from Node_BDD.graph import Node_BDD
from Node_BDD.relation import Relation as Neo4jRelation
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List
from langchain_core.prompts import ChatPromptTemplate
import Generation.model_provider as ge

class Relation(BaseModel):
    source: str = Field(description="Name of the source node")
    target: str = Field(description="Name of the target node")
    type: str = Field(description="Type of the relationship (e.g., USES, BELONGS_TO, etc.)")
    description: str = Field(description="Description of the relationship")

class Node(BaseModel):
    nom: str
    description: str
    type: str
    category: str

class GraphSchema(BaseModel):
    nodes: List[Node]
    relations: List[Relation]

class EspaceRechercheNode(Noeud):
    def __init__(self, node_bdd ,id : str, sujet : str, objectif : str, couleur_espace : str ):
        self.id =id
        self.sujet = sujet 
        self.objectif = objectif
        self.noeud = Noeud(couleur_espace,sujet,objectif)
        self.noeud.cree(node_bdd)

    def generate_graph_from_prompt(self, context: str, models: str = "ministral-8b-instruct-2410"):
        parser = PydanticOutputParser(pydantic_object=GraphSchema)
        format_instructions = parser.get_format_instructions().replace("{", "{{").replace("}", "}}")

        system_prompt = (
        "You are an intelligent AI research assistant. Your job is to help users clarify and deepen their research by generating a knowledge graph structure: nodes (key concepts) and relationships (how these concepts are linked).\n"
        "\n"
        "INSTRUCTIONS:\n"
        "- Carefully analyze the provided context.\n"
        "- For each essential term or concept, generate a node with: nom, description, type, and category.\n"
        "- For each relevant relationship, generate a relation with: source (node name), target (node name), type (relationship type), and description.\n"
        "- Output a single JSON object with two keys: 'nodes' (list of node objects) and 'relations' (list of relation objects).\n"
        "- DO NOT add any explanation or text outside the JSON.\n"
        f"- Respond values must only be in the prompt language.\n"
        "\n"
        "EXAMPLE OUTPUT:\n"
        "{{\n"
        "  \"nodes\": [\n"
        "    {{\"nom\": \"NeoJ4\", \"description\": \"A graph database management system.\", \"type\": \"software\", \"category\": \"technology\"}},\n"
        "    {{\"nom\": \"data storage\", \"description\": \"The process of saving digital information in a persistent medium.\", \"type\": \"concept\", \"category\": \"computer science\"}}\n"
        "  ],\n"
        "  \"relations\": [\n"
        "    {{\"source\": \"NeoJ4\", \"target\": \"data storage\", \"type\": \"USES\", \"description\": \"NeoJ4 uses data storage to persist information.\"}}\n"
        "  ]\n"
        "}}\n"
        f"{format_instructions}\n"
    )


        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", "{input}")
        ])

        chain = prompt | ge.get_model(models) | parser

        try:
            response = chain.invoke({"input": context})
            return response
        except Exception as e:
            print(f"Erreur de parsing : {e}")
            return None
        
    def add_graph_NodeBDD(self, node_bdd, graph_data, color_map=None):
        if color_map is None:
            color_map = {}

        name_to_id = {}

        # 1. Création des noeuds
        for node in getattr(graph_data, 'nodes', []):
            couleur = color_map.get(getattr(node, 'category', None), "grey")
            nom = getattr(node, 'nom', None)
            description = getattr(node, 'description', "")
            n = Noeud(couleur, nom, description)
            if n.cree(node_bdd):
                name_to_id[nom] = n.id

                if n.id != self.noeud.id:
                    auto_rel = Neo4jRelation(
                        source_id=n.id,
                        target_id=self.noeud.id,
                        type="APPARTIENT_A",
                        description="Lien automatique avec le nœud principal"
                    )
                    auto_rel.create(node_bdd)
            else:
                print(f"[ERREUR] Impossible de créer le noeud {nom}")

        # 2. Création des relations du graphe
        for rel in getattr(graph_data, 'relations', []):
            source_name = getattr(rel, 'source', None)
            target_name = getattr(rel, 'target', None)
            rel_type = getattr(rel, 'type', None)
            description = getattr(rel, 'description', "")
            source_id = name_to_id.get(source_name)
            target_id = name_to_id.get(target_name)
            if not source_id or not target_id:
                print(f"[WARN] Impossible de trouver les IDs pour la relation {source_name} -> {target_name}")
                continue
            relation_obj = Neo4jRelation(
                source_id=source_id,
                target_id=target_id,
                type=rel_type,
                description=description
            )
            if not relation_obj.create(node_bdd):
                print(f"[ERREUR] Impossible de créer la relation {source_name} -> {target_name} ({rel_type})")



#node_bdd = Node_BDD()
#test_espace = EspaceRechercheNode(node_bdd,"Crée un moteur de recherche augmenté par IA","FAire un concurent concret à perplexity et you.com en ajoutant la possibilité de visualisé la recherche par un graphe.","#267dc5")

#context = test_espace.generate_graph_from_prompt(""" Crawl4AI est un outil de crawling et de scraping très complet qui vise à générer du Markdown propre, idéal pour les pipelines RAG (Retrieval-Augmented Generation) ou une ingestion directe dans des modèles d'IA. Il permet également la structuration de données (Structured)[https://docs.crawl4ai.com/]. Crawl4AI peut être utilisé avec différents fournisseurs de LLM (Large Language Models), comme Azure OpenAI, en se référant au manuel des fournisseurs liteLLM (Lightweight Language Models) (https://www.pondhouse-data.com/blog/webcrawling-with-crawl4ai).Crawl4AI est une initiative open source qui vise à fournir des outils pour extraire et structurer les données, favorisant ainsi une économie de partage des données. L'outil est conçu pour être utilisé par des individus comme des organisations (https://pypi.org/project/Crawl4AI/).Bien qu'il soit puissant avec des mécanismes intégrés d'évasion de bot, Crawl4AI ne peut pas contourner les sites très protégés comme G2 qui utilisent des mesures anti-bot et anti-scraping rigoureuses (https://brightdata.com/blog/web-data/crawl4ai-and-deepseek-web-scraping). """)


#print(context)
#test_espace.add_graph_NodeBDD(node_bdd,context)