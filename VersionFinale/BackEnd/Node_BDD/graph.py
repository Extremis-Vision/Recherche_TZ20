from neo4j import GraphDatabase
import os
from dotenv import load_dotenv
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from Node_BDD.relation import Relation


chemin_env = os.path.join(os.path.dirname(__file__), '..', '..', '.env')

load_dotenv(chemin_env)

class BDD_Node:
    def __init__(self):
        self.driver = GraphDatabase.driver(os.getenv('NEO4J_URI'), auth=(os.getenv('NEO4J_USER'), os.getenv('NEO4J_PASSWORD')))

    def get_noeuds(self) -> list[dict]:
        """Retrieve all nodes from the database using a custom id property."""
        with self.driver.session() as session:
            query = "MATCH (n:Node) RETURN n"
            result = session.run(query)
            noeuds = []
            for record in result:
                node_dict = dict(record["n"])
                # Ensure each node has a unique id property
                noeuds.append(node_dict)
            return noeuds

    def get_relations(self) -> list[dict]:
        """Retourne toutes les relations entre les n?uds."""
        with self.driver.session() as session:
            query = """
            MATCH (a:Node)-[r]->(b:Node)
            RETURN a.name AS source, b.name AS target, type(r) AS type, r.description AS description
            """
            result = session.run(query)
            return [
                {
                    "source": record["source"],
                    "target": record["target"],
                    "type": record["type"],
                    "description": record["description"]
                }
                for record in result
            ]
        
    @classmethod
    def load_relations_of_node(cls, node_bdd, node_id: str, direction: str = "both") -> list['Relation']:
        """
        Charge toutes les relations d'un n?ud donn�.
        :param node_id: ID du n?ud
        :param direction: "out" (relations sortantes), "in" (relations entrantes), "both" (les deux)
        :return: liste de relations
        """
        with node_bdd.driver.session() as session:
            if direction == "out":
                query = """
                MATCH (a:Node {id: $node_id})-[r]->(b:Node)
                RETURN a.id AS source_id, b.id AS target_id, type(r) AS type, r.description AS description
                """
            elif direction == "in":
                query = """
                MATCH (a:Node)<-[r]-(b:Node {id: $node_id})
                RETURN a.id AS target_id, b.id AS source_id, type(r) AS type, r.description AS description
                """
            else:  # both
                query = """
                MATCH (a:Node)-[r]-(b:Node)
                WHERE a.id = $node_id OR b.id = $node_id
                RETURN DISTINCT
                    a.id AS source_id,
                    b.id AS target_id,
                    type(r) AS type,
                    r.description AS description
                """
            result = session.run(query, node_id=node_id)
            # On s'assure que source_id et target_id sont bien plac�s selon la direction
            if direction == "in":
                relations = [
                    cls(
                        source_id=record["source_id"],
                        target_id=record["target_id"],
                        type=record["type"],
                        description=record["description"]
                    )
                    for record in result
                ]
            else:
                relations = [
                    cls(
                        source_id=record["source_id"],
                        target_id=record["target_id"],
                        type=record["type"],
                        description=record["description"]
                    )
                    for record in result
                ]
            return relations

    @staticmethod
    def convert_id(id_value):
        """
        Convertit l'ID en entier si c'est une chaîne composée uniquement de chiffres.
        Retourne la valeur telle quelle sinon.
        """
        if isinstance(id_value, str):
            # Enlever les espaces et vérifier si uniquement des chiffres
            cleaned_id = id_value.strip()
            if cleaned_id.isdigit():
                return int(cleaned_id)
        return id_value

    def parse_graph_neo4j(self) -> dict:
        """Parse le graphe Neo4j et retourne les nœuds et les arêtes."""
        nodes = []
        edges = []

        with self.driver.session() as session:
            # Récupérer les nœuds
            result_nodes = session.run("""
                MATCH (n:Node)
                RETURN n, id(n) as neo4j_id
            """)
            
            for record in result_nodes:
                node = record["n"]
                node_props = dict(node)
                
                # Utiliser l'ID existant ou créer un nouveau
                node_id = str(node_props.get("id", record["neo4j_id"]))
                
                node_data = {
                    "id": node_id,
                    "displayLabel": str(node_props.get("nom", "") or node_props.get("name", "") or node_id),
                    "name": str(node_props.get("name", "")),
                    "nom": str(node_props.get("nom", "")),
                    "backgroundcolor": str(node_props.get("couleur", "") or node_props.get("backgroundcolor", "#267dc5")),
                    "description": str(node_props.get("description", ""))
                }
                nodes.append({"data": node_data})

            # Récupérer les arêtes
            result_edges = session.run("""
                    MATCH (a:Node)-[r]->(b:Node)
                    RETURN a.id as source, b.id as target, type(r) as type, 
                        r.description as description, id(r) as edge_id
                """)

            edges = []
            for record in result_edges:
                source_id = str(record["source"])
                target_id = str(record["target"])
                edge_id = str(record["edge_id"])  # <-- juste le chiffre, sans préfixe

                edge_data = {
                    "id": edge_id,  # id numérique de la relation
                    "source": source_id,
                    "target": target_id,
                    "label": str(record["type"]),
                    "type": str(record["type"]),
                    "description": str(record["description"] or "")
                }
                edges.append({"data": edge_data})

                print("Nodes:", nodes)  # Debug
                print("Edges:", edges)  # Debug
                return {"nodes": nodes, "edges": edges}
            


#Exemple d'utilisation 
#node_bdd = BDD_Node()
#print(node_bdd.parse_graph_neo4j())