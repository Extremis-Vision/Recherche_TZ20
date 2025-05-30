import os
import chromadb
from chromadb.config import Settings
from dotenv import load_dotenv

load_dotenv('.env')

host = os.getenv("CHROMA_SERVER_HOST", "localhost")
port = int(os.getenv("CHROMA_SERVER_PORT", "8000"))
collection_name = os.getenv("CHROMA_COLLECTION_NAME", "my_collection")

client = chromadb.HttpClient(
    host=host,
    port=port,
    settings=Settings()
)

collection = client.get_or_create_collection(name=collection_name)
