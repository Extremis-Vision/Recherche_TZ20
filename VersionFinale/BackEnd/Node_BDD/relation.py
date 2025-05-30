from dataclasses import dataclass
from typing import Optional, Dict

@dataclass
class Relation:
    source_id: str          # ID du n?ud source
    target_id: str          # ID du n?ud cible
    type: str               # Type de la relation (ex: "RELATED_TO")
    description: str        # Description de la relation (optionnelle)

    def to_dict(self) -> Dict[str, str]:
        """Convertit la relation en dictionnaire."""
        return {
            "source_id": self.source_id,
            "target_id": self.target_id,
            "type": self.type,
            "description": self.description
        }

    def create(self, node_bdd) -> bool:
        """Cr�e la relation dans la base de donn�es Neo4j."""
        with node_bdd.driver.session() as session:
            query = """
            MATCH (a:Node {id: $source_id}), (b:Node {id: $target_id})
            MERGE (a)-[r:%s {description: $description}]->(b)
            RETURN r
            """ % self.type
            result = session.run(query, **self.to_dict())
            return result.single() is not None

    def supprimer(self, node_bdd) -> bool:
        """Supprime la relation de la base de donn�es Neo4j."""
        with node_bdd.driver.session() as session:
            query = """
            MATCH (a:Node {id: $source_id})-[r:%s]->(b:Node {id: $target_id})
            WHERE r.description = $description
            DELETE r
            """ % self.type
            session.run(query, **self.to_dict())
            return True

    @classmethod
    def load_relation(cls, node_bdd, source_id: str, target_id: str, rel_type: str) -> Optional['Relation']:
        """
        Charge une relation sp�cifique entre deux n?uds.
        :param source_id: ID du n?ud source
        :param target_id: ID du n?ud cible
        :param rel_type: type de la relation
        :return: la relation, ou None si elle n'existe pas
        """
        with node_bdd.driver.session() as session:
            query = """
            MATCH (a:Node {id: $source_id})-[r:%s]->(b:Node {id: $target_id})
            RETURN a.id AS source_id, b.id AS target_id, type(r) AS type, r.description AS description
            """ % rel_type
            result = session.run(query, source_id=source_id, target_id=target_id)
            record = result.single()
            if record is None:
                return None
            return cls(
                source_id=record["source_id"],
                target_id=record["target_id"],
                type=record["type"],
                description=record["description"]
            )

