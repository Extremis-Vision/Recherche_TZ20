import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from Node_BDD.graph import BDD_Node
from Node_BDD.noeud import Noeud

node_bdd = BDD_Node()

# Print the graph data to verify the nodes
print(node_bdd.parse_graph_neo4j())

# Attempt to load a node
node_id = "4:4bb8bff4-fd87-4153-a024-5f8232de8d80:93"
noeud_current = Noeud.load(node_bdd, node_id)

if noeud_current:
    print(noeud_current.dico())
    # Attempt to delete the node
    if noeud_current.supprimer(node_bdd):
        print(f"Node with ID {node_id} deleted successfully.")
    else:
        print(f"Failed to delete node with ID {node_id}.")
else:
    print(f"No node found with ID {node_id}")
