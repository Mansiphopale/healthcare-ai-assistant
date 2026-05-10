import os
from dotenv import load_dotenv

load_dotenv()

# LLM - Ollama
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
LLM_MODEL = os.getenv("LLM_MODEL", "mistral")

# Embeddings
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

# Paths
VECTOR_STORE_PATH = os.getenv("VECTOR_STORE_PATH", "./vector_store")
DATA_FOLDER = os.getenv("DATA_FOLDER", "./data")

# App
APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
APP_PORT = int(os.getenv("APP_PORT", 8000))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")