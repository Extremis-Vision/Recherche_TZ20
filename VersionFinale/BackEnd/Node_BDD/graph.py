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

    def parse_graph_neo4j(self) -> dict:
        """Parse le graphe Neo4j et retourne les nœuds et les arêtes."""
        nodes = []
        edges = []

        with self.driver.session() as session:
            # Récupérer les nœuds avec leurs propriétés
            result_nodes = session.run("""
                MATCH (n:Node) 
                RETURN n, ID(n) as neo4j_id,
                    CASE WHEN n.name IS NOT NULL THEN n.name 
                         WHEN n.nom IS NOT NULL THEN n.nom 
                         ELSE toString(ID(n)) END as displayName,
                    COALESCE(n.backgroundcolor, '#267dc5') as bgcolor
            """)
            
            # Map pour stocker les IDs des nœuds
            node_ids = {}
            
            for record in result_nodes:
                node = record["n"]
                node_props = dict(node)
                node_id = node_props.get("id", str(record["neo4j_id"]))
                node_ids[record["neo4j_id"]] = node_id
                
                node_data = {
                    "id": node_id,
                    "name": node_props.get("name", ""),
                    "nom": node_props.get("nom", ""),
                    "displayLabel": record["displayName"],
                    "backgroundcolor": record["bgcolor"],
                    "description": node_props.get("description", "")
                }
                nodes.append({"data": node_data})

            # Récupérer les arêtes avec les IDs des nœuds source et cible
            result_edges = session.run("""
                MATCH (a:Node)-[r]->(b:Node)
                RETURN ID(a) as source_id, ID(b) as target_id,
                       a.id as source_custom_id, b.id as target_custom_id,
                       type(r) as type, r.description as description
            """)
            
            for record in result_edges:
                source_id = node_ids.get(record["source_id"]) or record["source_custom_id"]
                target_id = node_ids.get(record["target_id"]) or record["target_custom_id"]
                
                if source_id and target_id:  # Ne créer l'arête que si les deux IDs existent
                    edge_data = {
                        "id": f"edge-{source_id}-{target_id}",
                        "source": source_id,
                        "target": target_id,
                        "label": record["type"],
                        "type": record["type"],
                        "description": record["description"] or ""
                    }
                    edges.append({"data": edge_data})

        return {"nodes": nodes, "edges": edges}
    


#Exemple d'utilisation 
#node_bdd = BDD_Node()
#print(node_bdd.parse_graph_neo4j())