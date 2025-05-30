from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

chemin_env = os.path.join(os.path.dirname(__file__), '..', '..', '.env')

load_dotenv(chemin_env)

AIURL = os.getenv("AI_URL", "http://localhost:1234/v1")

def get_model(model_name: str) -> ChatOpenAI:
    return ChatOpenAI(
        api_key="lm-studio",  # ou os.getenv("AI_API_KEY", "lm-studio") si tu veux une cl� configurable
        base_url=AIURL,
        model=model_name,
        temperature=0.7,
        max_tokens=4096,
        streaming=True
    )