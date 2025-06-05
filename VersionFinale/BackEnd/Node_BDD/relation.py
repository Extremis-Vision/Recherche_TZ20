class Relation:
    def __init__(self, source_id: str, target_id: str, type: str, description: str = "", id : int = None):
        self.source_id = source_id
        self.target_id = target_id
        self.id = id
        self.type = type.replace(" ", "_")  # Remplacer les espaces par des underscores
        self.description = description

    def to_dict(self):
        return {
            "id": self.id,
            "source_id": self.source_id,
            "target_id": self.target_id,
            "type": self.type,
            "description": self.description
        }

    def create(self, node_bdd):
        """Crée la relation dans la base de données Neo4j."""
        with node_bdd.driver.session() as session:
            query = """
                MATCH (a:Node {id: $source_id})
                MATCH (b:Node {id: $target_id})
                MERGE (a)-[r:`%s` {description: $description}]->(b)
                RETURN r
            """ % self.type  # Utilisation de la chaîne formatée de manière sécurisée
            
            try:
                session.run(
                    query,
                    source_id=self.source_id,
                    target_id=self.target_id,
                    description=self.description
                )
                return True
            except Exception as e:
                print("Erreur lors de la création de la relation:", e)
                raise e

    def supprimer(self, node_bdd):
        """Supprime la relation de la base de données Neo4j à partir de son id interne."""
        with node_bdd.driver.session() as session:
            query = """
                MATCH ()-[r]->()
                WHERE elementId(r) = $rel_id
                DELETE r
            """
            session.run(query, rel_id=self.id)
            return True


    @classmethod
    def load_relation_by_id(cls, node_bdd, rel_id: int):
        """Charge une relation à partir de son id interne Neo4j (elementId)."""
        with node_bdd.driver.session() as session:
            query = (
                """
                MATCH ()-[r]->()
                WHERE elementId(r) = $rel_id
                RETURN type(r) AS type, r AS rel, elementId(r) AS rel_id, startNode(r).id AS source_id, endNode(r).id AS target_id
                """
            )
            result = session.run(query, rel_id=rel_id)
            record = result.single()
            if record is None:
                return None
            # On récupère les propriétés de la relation (rel)
            rel_props = dict(record["rel"])
            return cls(
                rel_id=record["rel_id"],
                type=record["type"],
                source_id=record["source_id"],
                target_id=record["target_id"],
                **rel_props  # inclut toutes les propriétés de la relation
            )

