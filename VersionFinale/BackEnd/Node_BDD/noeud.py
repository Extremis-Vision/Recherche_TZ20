class Noeud:
    def __init__(self, couleur: str, nom: str, description: str,  id: str = None):
        self.id = None  # L'id sera défini après création dans la BDD
        self.couleur = couleur
        self.nom = nom
        self.description = description

    def dico(self):
        return {
            "id": self.id,
            "backgroundcolor": self.couleur,
            "nom": self.nom,
            "description": self.description
        }
    
    def get_id(self):
        return self.id
    
    def get_couleur(self):
        return self.couleur

    def get_nom(self):
        return self.nom

    def get_description(self):
        return self.description

    def cree(self, node_bdd):
        """Crée le noeud dans Neo4j et met à jour self.id avec l'id généré."""
        if self.node == None :
            with node_bdd.driver.session() as session:
                properties = self.to_dict()
                properties.pop("id", None)
                props = ", ".join([f"{k}: ${k}" for k in properties])
                query = (
                    f"CREATE (n:Node {{ {props}, id: randomUUID() }}) "
                    f"RETURN n.id AS id"
                )
                try:
                    result = session.run(query, **properties)
                    data = result.single()
                    print(f"[DEBUG] data: {data}, type: {type(data)}")
                    if data:
                        # Neo4j Record: accès par index ou méthode
                        try:
                            self.id = data["id"]
                        except (KeyError, TypeError):
                            self.id = data.get("id", None)
                        return True if self.id else False
                    else:
                        print(f"[DEBUG] Création échouée pour {self.nom}. Query: {query}, Properties: {properties}, Data: {data}")
                        return False
                except Exception as e:
                    print(f"[EXCEPTION] Erreur lors de la création du noeud {self.nom}: {e}")
                    return False
        else :
             with node_bdd.driver.session() as session:
                properties = self.to_dict()
                props = ", ".join([f"{k}: ${k}" for k in properties])
                query = (
                    f"CREATE (n:Node {{ {props} }}) "
                    f"RETURN n.id AS id"
                )
                try:
                    result = session.run(query, **properties)
                    data = result.single()
                    print(f"[DEBUG] data: {data}, type: {type(data)}")
                    return data is not None
                except Exception as e:
                    print(f"[EXCEPTION] Erreur lors de la création du noeud {self.nom} (id imposé): {e}")
                    return False


    def supprimer(self, node_bdd):
        """Supprime le noeud de Neo4j (si self.id existe)."""
        if not self.id:
            print("Impossible de supprimer : id inconnu.")
            return False
        with node_bdd.driver.session() as session:
            query = "MATCH (n:Node {id: $id}) DELETE n"
            session.run(query, id=self.id)
            return True

    @classmethod
    def load(cls, node_bdd, id_noeud: str):
        """Charge un noeud depuis Neo4j, retourne un objet Noeud ou None."""
        with node_bdd.driver.session() as session:
            query = "MATCH (n:Node {id: $id}) RETURN n"
            result = session.run(query, id=id_noeud)
            data = result.single()
            if data is None:
                return None
            node_dict = dict(data["n"])
            n = cls(
                couleur=node_dict["couleur"],
                nom=node_dict["nom"],
                description=node_dict["description"]
            )
            n.id = node_dict["id"]
            return n



#Exemple
#from graph import Node_BDD
#node_bdd = Node_BDD()
#n = Noeud(Color("blue"), "Neo4j", "Base de données graphe")
#n.cree(node_bdd)