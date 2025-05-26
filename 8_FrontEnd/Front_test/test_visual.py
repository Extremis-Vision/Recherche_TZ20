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
        # Récupère tous les nœuds et leurs propriétés
        result_nodes = session.run("MATCH (n) RETURN n")
        for record in result_nodes:
            node = record["n"]
            node_id = str(node.id)
            # Récupère toutes les propriétés du nœud
            props = dict(node)
            props["id"] = node_id  # Ajoute l'id pour l'identification côté JS
            nodes[node_id] = props
        # Récupère toutes les arêtes
        result_edges = session.run("MATCH (a)-[r]->(b) RETURN a, b, r")
        for record in result_edges:
            source = str(record["a"].id)
            target = str(record["b"].id)
            edges.append({"data": {"source": source, "target": target}})
    node_list = [{"data": node} for node in nodes.values()]
    return {"nodes": node_list, "edges": edges}


def ajouter_noeud(label, properties):
    with driver.session() as session:
        props = ", ".join([f"{k}: ${k}" for k in properties])
        query = f"CREATE (n:{label} {{ {props} }}) RETURN n"
        result = session.run(query, **properties)
        return result.single()[0]

@app.route('/graph')
def get_graph():
    return jsonify(parse_graph_neo4j())

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/add_node', methods=['POST'])
def add_node():
    data = request.get_json()
    label = data.get('label', 'Noeud')
    properties = data.get('properties', {})
    node = ajouter_noeud(label, properties)
    return jsonify({"status": "success", "node": dict(node)}), 201

if __name__ == '__main__':
    app.run(debug=True)