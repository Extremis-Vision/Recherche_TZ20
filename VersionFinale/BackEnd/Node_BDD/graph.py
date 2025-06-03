from neo4j import GraphDatabase
import os
from dotenv import load_dotenv
from .relation import Relation

chemin_env = os.path.join(os.path.dirname(__file__), '..', '..', '.env')

load_dotenv(chemin_env)

class BDD_Node:
    def __init__(self):
        self.driver = GraphDatabase.driver(os.getenv('NEO4J_URI'), auth=(os.getenv('NEO4J_USER'), os.getenv('NEO4J_PASSWORD')))

    def get_noeuds(self) -> list[dict]:
        """Retourne tous les n?uds de la base de donn�es."""
        with self.driver.session() as session:
            query = "MATCH (n:Node) RETURN n, ID(n) AS internal_id"
            result = session.run(query)
            noeuds = []
            for record in result:
                node_dict = dict(record["n"])
                node_dict["internal_id"] = record["internal_id"]
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

    
    


#Exemple d'utilisation 
#node_bdd = GraphDatabase()
#print(node_bdd.get_noeuds())