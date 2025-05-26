from llama_index.llms.lmstudio import LMStudio
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings

# 1. Charger et indexer vos documents
documents = SimpleDirectoryReader("./").load_data()

# 2. Configurer l'embedding model pour pointer vers LM Studio
embed_model = OpenAIEmbedding(
    api_key="lm-studio",  # Peu importe, LM Studio n'utilise pas la clé
    api_base="http://localhost:1234/v1",
    model_name="nomic-ai/nomic-embed-text-v1.5-GGUF"  # Le nom exact du modèle d'embedding chargé dans LM Studio
)
Settings.embed_model = embed_model

# 3. Créer l'index vectoriel AVEC l'embedding model LM Studio
index = VectorStoreIndex.from_documents(documents)

# 4. Configurer le LLM pour pointer vers LM Studio
llm = LMStudio(
    model_name="ministral-8b-instruct-2410",  # Adapter au nom exact du modèle LLM chargé
    base_url="http://localhost:1234/v1",
    temperature=0.7,
)

# 5. Créer un moteur de requête RAG
query_engine = index.as_query_engine(llm=llm)

# 6. Interroger votre base documentaire avec RAG
response = query_engine.query("Quels outils de recherche internet par ia sont cité dans le projet ?")
print(response)
