import generation as gen
import recherche as rec
import node_bdd 

question = "Oui, Neo4j permet d'enregistrer des données. Les fichiers de la base de données Neo4j sont stockés pour une durabilité à long terme et se trouvent par défaut dans le répertoire `data/databases/graph.db` (pour les versions 3.x+). Ces fichiers contiennent diverses informations sur les nœuds, relations et propriétés des graphes. Par exemple, vous pouvez trouver des fichiers comme `neostore.nodestore`, `neostore.propertystore`, etc., qui stockent différents types de données."
graph_data = gen.generate_graph(question)
print("graph_data:", graph_data)

if graph_data:
    node_bdd.create_graph_in_neo4j(graph_data)
    print("Graph created in Neo4j!")
else:
    print("Erreur lors de la génération du graphe.")