from llama_index.llms.lmstudio import LMStudio
from llama_index.core import SimpleDirectoryReader
import networkx as nx

# 1. Charger les documents
documents = SimpleDirectoryReader("./5_recherche_internet").load_data()

# 2. Configurer le LLM LM Studio
llm = LMStudio(
    model_name="mistral-8b-instruct-2410",  # Adapter au modèle chargé
    base_url="http://localhost:1234/v1"
)

# 3. Extraire les entités/relations (prompt engineering)
def extract_entities_relations(text):
    prompt = f"""Extract all entities and relationships in the following text. 
    Format: (Entity1)-[Relation]->(Entity2)
    Text: {text}
    """
    response = llm.complete(prompt)
    return response.text  # Adapter selon la sortie

# 4. Construire le graphe
G = nx.DiGraph()
for doc in documents:
    triples = extract_entities_relations(doc.text).split("\n")
    for triple in triples:
        if triple.strip():
            # Exemple de parsing simple : (A)-[rel]->(B)
            parts = triple.replace("(", "").replace(")", "").split("->[")
            if len(parts) == 2:
                entity1, rest = parts
                relation, entity2 = rest.split("]->")
                G.add_edge(entity1.strip(), entity2.strip(), relation=relation.strip())

# 5. Pour une question, extraire le sous-graphe pertinent et générer la réponse
def answer_with_graph(question):
    # Extraire les entités de la question (idem étape 3)
    entities = extract_entities_relations(question)
    # Utiliser le graphe pour retrouver les contextes pertinents
    # (Ici, exemple simple : récupérer les voisins)
    context = []
    for node in G.nodes:
        if node in question:
            neighbors = list(G.neighbors(node))
            for n in neighbors:
                context.append(f"{node} -[{G[node][n]['relation']}]-> {n}")
    # Générer la réponse avec le contexte
    prompt = f"Question: {question}\nContext:\n" + "\n".join(context)
    response = llm.complete(prompt)
    return response.text

print(answer_with_graph("Qu'est-ce que le projet Crawl4AI ?"))
