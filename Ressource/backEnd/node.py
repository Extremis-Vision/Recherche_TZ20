from neo4j import GraphDatabase

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "testyudsqdqs23"

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

def ajouter_noeud(label, properties):
    with driver.session() as session:
        props = ", ".join([f"{k}: ${k}" for k in properties])
        query = f"CREATE (n:{label} {{ {props} }}) RETURN n"
        result = session.run(query, **properties)
        return result.single()[0]

def supprimer_noeud(element_id):
    with driver.session() as session:
        query = "MATCH (n) WHERE n(n) = $id DELETE n"
        session.run(query, id=element_id)

def supprimer_noeud_nom(element_id):
    with driver.session() as session:
        query = "MATCH (n {nom: $nom}) DELETE n"
        session.run(query, nom=element_id)

def modifier_noeud(element_id, properties):
    try:
        with driver.session() as session:
            # Vérifier l'existence du nœud
            check_query = "MATCH (n) WHERE n.nom = $id RETURN n"
            check_result = session.run(check_query, id=element_id)
            if check_result.single() is None:
                print(f"Aucun nœud trouvé avec le nom '{element_id}'.")
                return None

            # Mettre à jour le nœud
            set_clause = ", ".join([f"n.{k} = ${k}" for k in properties])
            query = f"MATCH (n) WHERE n.nom = $id SET {set_clause} RETURN n"
            result = session.run(query, id=element_id, **properties)
            node = result.single()[0]
            return node
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")
        return None

