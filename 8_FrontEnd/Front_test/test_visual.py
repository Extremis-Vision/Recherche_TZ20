from flask import Flask, jsonify, send_from_directory, request
from neo4j import GraphDatabase

app = Flask(__name__)

# Config Neo4j
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "testyudsqdqs23"

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

def parse_graph_neo4j():
    nodes = {}
    edges = []
    with driver.session() as session:
        result_nodes = session.run("MATCH (n) RETURN n")
        for record in result_nodes:
            node = record["n"]
            node_id = str(node.element_id)  # Remplacer id par element_id
            props = dict(node)
            props["id"] = node_id
            nodes[node_id] = props
        result_edges = session.run("MATCH (a)-[r]->(b) RETURN a, b, r")
        for record in result_edges:
            source = str(record["a"].element_id)  # Remplacer id par element_id
            target = str(record["b"].element_id)  # Remplacer id par element_id
            rel_type = record["r"].type
            edges.append({
                "data": {
                    "source": source,
                    "target": target,
                    "label": rel_type
                }
            })
    node_list = [{"data": node} for node in nodes.values()]
    return {"nodes": node_list, "edges": edges}


@app.route('/edit_relation', methods=['POST'])
def edit_relation():
    data = request.get_json()
    source = data['source']         # elementId du noeud source (string)
    target = data['target']         # elementId du noeud cible (string)
    old_label = data['old_label']   # ex: "Friends"
    new_label = data['new_label']   # ex: "Colleagues"

    with driver.session() as session:
        # Supprime l’ancienne relation
        query_delete = (
            f"MATCH (a)-[r:{old_label}]->(b) "
            "WHERE elementId(a) = $source AND elementId(b) = $target "
            "DELETE r"
        )
        session.run(query_delete, source=source, target=target)

        # Crée la nouvelle relation
        query_create = (
            f"MATCH (a), (b) "
            "WHERE elementId(a) = $source AND elementId(b) = $target "
            f"CREATE (a)-[r:{new_label}]->(b)"
        )
        session.run(query_create, source=source, target=target)

    return jsonify({"status": "success"})

@app.route('/graph')
def get_graph():
    return jsonify(parse_graph_neo4j())

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

def ajouter_noeud(label, properties):
    with driver.session() as session:
        props = ", ".join([f"{k}: ${k}" for k in properties])
        query = f"CREATE (n:{label} {{ {props} }}) RETURN n"
        result = session.run(query, **properties)
        return result.single()[0]

@app.route('/add_relation', methods=['POST'])
def add_relation():
    data = request.get_json()
    id_source = data.get('id_source')
    id_cible = data.get('id_cible')
    nom_relation = data.get('nom_relation', 'RELATION')
    properties = data.get('properties', {})
    relation = ajouter_relation(id_source, id_cible, nom_relation, properties)
    if relation:
        return jsonify({"status": "success", "relation": relation}), 201
    else:
        return jsonify({"status": "error", "message": "Relation non créée"}), 400

def ajouter_relation(id_source, id_cible, nom_relation, properties=None):
    try:
        properties = properties or {}
        props = ", ".join([f"{k}: ${k}" for k in properties])
        props_str = f"{{ {props} }}" if properties else ""
        query = (
            "MATCH (a), (b) "
            "WHERE elementId(a) = $id_source AND elementId(b) = $id_cible "
            f"CREATE (a)-[r:{nom_relation} {props_str}]->(b) "
            "RETURN r"
        )
        with driver.session() as session:
            params = {"id_source": id_source, "id_cible": id_cible, **properties}
            result = session.run(query, **params)
            rel = result.single()
            if rel:
                return dict(rel["r"])
            else:
                return None
    except Exception as e:
        print("Erreur Cypher:", e)
        return None


@app.route('/add_node', methods=['POST'])
def add_node():
    data = request.get_json()
    label = data.get('label', 'Noeud')
    properties = data.get('properties', {})
    node = ajouter_noeud(label, properties)
    return jsonify({"status": "success", "node": dict(node)}), 201

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
