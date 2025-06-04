class Relation:
    def __init__(self, source_id: str, target_id: str, type: str, description: str = ""):
        self.source_id = source_id
        self.target_id = target_id
        self.type = type.replace(" ", "_")  # Remplacer les espaces par des underscores
        self.description = description

    def to_dict(self):
        return {
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
        """Supprime la relation de la base de données Neo4j."""
        with node_bdd.driver.session() as session:
            query = (
                f"""
                MATCH (a:Node {{id: $source_id}})-[r:{self.type}]->(b:Node {{id: $target_id}})
                WHERE r.description = $description
                DELETE r
                """
            )
            session.run(query, **self.to_dict())
            return True

    @classmethod
    def load_relation(cls, node_bdd, source_id: str, target_id: str, rel_type: str):
        """Charge une relation spécifique entre deux nœuds."""
        with node_bdd.driver.session() as session:
            query = (
                f"""
                MATCH (a:Node {{id: $source_id}})-[r:{rel_type}]->(b:Node {{id: $target_id}})
                RETURN a.id AS source_id, b.id AS target_id, type(r) AS type, r.description AS description
                """
            )
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
