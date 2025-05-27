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

def create_graph_in_neo4j(graph_data):
    with driver.session() as session:
        # Créer les nœuds
        for node in graph_data.nodes:
            properties = {
                "nom": node.nom,  # Utilisation de 'nom' au lieu de 'name'
                "description": node.description,
                "type": node.type,
                "category": node.category
            }
            session.run(
                "MERGE (n:Node {nom: $nom}) "  # Utilisation de 'nom' au lieu de 'name'
                "SET n.description = $description, n.type = $type, n.category = $category",
                **properties
            )
        # Créer les relations
        for rel in graph_data.relations:
            session.run(
                f"MATCH (a:Node {{nom: $source}}), (b:Node {{nom: $target}}) "  # Utilisation de 'nom' au lieu de 'name'
                f"MERGE (a)-[r:{rel.type}]->(b) "
                f"SET r.description = $description",
                {"source": rel.source, "target": rel.target, "description": rel.description}
            )
