import generation as gen
import recherche as rec
import node_bdd 


question = "What quantum programming should learn from software engineering ? "
keywords = gen.get_key_word_search(question,3)

print("Keywords:", keywords)
content = rec.simple_search(question,keywords,5)

graph_data = gen.generate_graph(content)
if graph_data:
    node_bdd.create_graph_in_neo4j(graph_data)
    print("Graph created in Neo4j!")
else:
    print("Erreur lors de la génération du graphe.")