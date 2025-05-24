import sys
from typing import List
import lmstudio as lms
from chromadb import Client
import chromadb
from openai import OpenAI
import CallTemplate


def divide_data_to_chunks(text: str, target_size : int = 1000) -> List[str]:
    chunks = []
    current_chunk = ""
    current_size = 0
    
    # Diviser le texte en phrases (séparation par point)
    sentences = text.split('.')
    
    for sentence in sentences:
        # Ajouter le point qui a été retiré par le split
        sentence = sentence.strip() + '.'
        sentence_size = len(sentence)
        
        if current_size + sentence_size > target_size and current_chunk:
            # Si l'ajout de la phrase dépasse la taille cible et qu'on a déjà du contenu
            chunks.append(current_chunk.strip())
            current_chunk = sentence
            current_size = sentence_size
        else:
            # Sinon, ajouter la phrase au chunk actuel
            current_chunk += ' ' + sentence
            current_size += sentence_size
    
    # Ajouter le dernier chunk s'il reste du contenu
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks

def create_chunks(contenue: str,target_size: int = 1000):
    allChunks = []

    for info in contenue :
        allChunks += divide_data_to_chunks(info["markdown"],target_size)

    return allChunks 

def create_embeding(chunks: List[str]) -> List[List[float]]:
    text_embed = []
    model = lms.embedding_model("nomic-embed-text-v1.5")
    for chunk in chunks:
        embedding = model.embed(chunk)
        text_embed.append(embedding)
    return text_embed

def store_embeddings(chunks: List[str], embeddings: List[List[float]], collection_name="my_collection"):
    client = chromadb.Client()
    try:
        collection = client.get_collection(name=collection_name)
    except:
        collection = client.create_collection(name=collection_name)
    
    # Convert embeddings to correct format
    embeddings = [list(map(float, emb)) for emb in embeddings]
    
    # Add documents with their embeddings
    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=[f"doc_{i}" for i in range(len(chunks))]
    )
    return collection


def get_response_from_raginfo(query: str, collection, model_name: str = "gemma-3-12b-it-qat"):
    # Create query embedding
    model = lms.embedding_model("nomic-embed-text-v1.5")
    query_embedding = list(map(float, model.embed(query)))
    
    # Search for relevant documents
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5
    )
    
    if not results['documents']:
        return "No relevant documents found."
    
    # Build context for LM Studio
    context = "\n".join(results['documents'][0])
    prompt = f"""
    Please answer this question: {query}
    Answer using only the information provided in the context."""
    
    # Get model response
    response = CallTemplate.response_with_context(prompt, context, model_name)
    return response



def get_RAG_response(contenu : str , model : str =  "gemma-3-12b-it-qat"):
    try:
        print("Création des chunks...")
        chunks = create_chunks(contenu, target_size=500)
        
        print("Création des embeddings...")
        embeddings = create_embeding(chunks)
        
        print("Stockage des embeddings...")
        collection = store_embeddings(chunks, embeddings)
        
        question = str(input("Donné la question sur la donnée donné :"))
        response = get_response_from_raginfo(question, collection, model)
        
        if response:
            print(f"\nQuestion: {question}")
            print(f"Réponse: {response}")
        else:
            print("Erreur: Pas de réponse reçue de LM Studio")
            
    except Exception as e:
        print(f"Erreur inattendue: {e}")
        sys.exit(1)