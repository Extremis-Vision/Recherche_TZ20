import uuid
from dataclasses import dataclass
from typing import Optional, Dict

class Color:
    def __init__(self, value: str):
        self.value = value

@dataclass
class Noeud:
    id: str
    couleur: Color
    name: str
    description: str

    @classmethod
    def create_new(cls, couleur: Color, name: str, description: str) -> 'Noeud':
        """Cr�e un nouveau noeud avec un UUID g�n�r� automatiquement."""
        return cls(str(uuid.uuid4()), couleur, name, description)

    def get_id(self) -> str:
        return self.id

    def get_couleur(self) -> Color:
        return self.couleur

    def get_name(self) -> str:
        return self.name

    def get_description(self) -> str:
        return self.description

    def to_dict(self) -> Dict[str, str]:
        return {
            "id": self.id,
            "couleur": self.couleur.value,
            "name": self.name,
            "description": self.description
        }

    def cree(self, node_bdd) -> bool:
        """Cr�e le noeud dans la base de donn�es Neo4j."""
        with node_bdd.driver.session() as session:
            properties = self.to_dict()
            props = ", ".join([f"{k}: ${k}" for k in properties])
            query = f"CREATE (n:Node {{ {props} }}) RETURN n"
            result = session.run(query, **properties)
            return result.single() is not None

    def supprimer(self, node_bdd) -> bool:
        """Supprime le noeud de la base de donn�es Neo4j."""
        with node_bdd.driver.session() as session:
            query = "MATCH (n:Node {id: $id}) DELETE n"
            result = session.run(query, id=self.id)
            # On ne v�rifie pas le r�sultat, car DELETE ne retourne rien
            # (mais on peut consid�rer que c'est un succ�s si aucune erreur n'est lev�e)
            return True
        
    @classmethod
    def load(cls, node_bdd, id_noeud: str) -> Optional['Noeud']:
        """Charge un noeud depuis la base de donn�es Neo4j."""
        with node_bdd.driver.session() as session:
            query = "MATCH (n:Node {id: $id}) RETURN n"
            result = session.run(query, id=id_noeud)
            data = result.single()
            if data is None:
                return None
            # On r�cup�re le noeud sous forme de dictionnaire
            node_dict = dict(data["n"])
            return cls(
                id=node_dict["id"],
                couleur=Color(node_dict["couleur"]),
                name=node_dict["name"],
                description=node_dict["description"]
            )

