from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import TextLoader
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import sys
from ask_ai import ask_ai, get_model

class CustomLLM:
    def __init__(self, model_name):
        self.model_name = model_name

    def __call__(self, prompt):
        system_prompt = "You are a helpful assistant. Answer based on the context provided."
        return ask_ai(system_prompt, prompt, self.model_name)

def create_rag_system(document_path, model_name):
    # Chargement et préparation des documents
    loader = TextLoader(document_path)
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)

    # Création des embeddings
    embeddings = HuggingFaceEmbeddings()
    
    # Création de la base vectorielle
    db = Chroma.from_documents(texts, embeddings)
    
    # Configuration du template de prompt
    template = """
    Utilise le contexte suivant pour répondre à la question.
    
    Contexte: {context}
    
    Question: {question}
    
    Réponse:"""
    
    prompt = PromptTemplate(template=template, input_variables=["context", "question"])
    
    # Création de la chaîne
    llm = CustomLLM(model_name)
    chain = LLMChain(llm=llm, prompt=prompt)
    
    return db, chain

def query_rag(question, db, chain):
    # Recherche des documents pertinents
    docs = db.similarity_search(question, k=3)
    context = "\n".join([doc.page_content for doc in docs])
    
    # Génération de la réponse
    response = chain.run(context=context, question=question)
    return response

if __name__ == "__main__":
    # Exemple d'utilisation
    models = get_model()
    if models:
        document_path = "RAG.md"
        db, chain = create_rag_system(document_path, models[0])
        
        question = "Votre question ici"
        answer = query_rag(question, db, chain)
        print(f"Réponse: {answer}")
