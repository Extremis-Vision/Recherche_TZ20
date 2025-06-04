class Noeud:
    def __init__(self, couleur: str, nom: str, description: str, id: str = None):
        self.id = id  # L'id sera défini après création dans la BDD
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
        if self.id is None:
            with node_bdd.driver.session() as session:
                properties = self.dico()
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
                        try:
                            self.id = data["id"]
                        except (KeyError, TypeError):
                            self.id = data.get("id", None)
                        return self.id is not None
                    else:
                        print(f"[DEBUG] Création échouée pour {self.nom}.")
                        return False
                except Exception as e:
                    print(f"[EXCEPTION] Erreur lors de la création du noeud {self.nom}: {e}")
                    return False
        else:
            with node_bdd.driver.session() as session:
                properties = self.dico()
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
        try:
            with node_bdd.driver.session() as session:
                query = "MATCH (n:Node {id: $id}) RETURN n"
                result = session.run(query, id=id_noeud)
                data = result.single()

                if data is None:
                    return None

                node_dict = dict(data["n"])
                print(f"[DEBUG] Node data: {node_dict}")

                # Clés obligatoires et variantes pour la couleur
                required_keys = ["nom", "description", "id"]
                color_keys = ["couleur", "color", "backgroundcolor"]

                # Vérifie la présence des clés obligatoires
                missing_keys = [key for key in required_keys if key not in node_dict]
                # Vérifie la présence d'au moins une clé couleur
                couleur = next((node_dict[c] for c in color_keys if c in node_dict), None)
                has_couleur = couleur is not None

                if not has_couleur:
                    missing_keys.append("couleur/color/backgroundcolor")

                if not missing_keys:
                    n = cls(
                        couleur=couleur,
                        nom=node_dict["nom"],
                        description=node_dict["description"]
                    )
                    n.id = node_dict["id"]
                    return n
                else:
                    return None
        except Exception as e:
            print(f"[EXCEPTION] Erreur lors du chargement du nœud avec l'ID {id_noeud}: {e}")
            return None
