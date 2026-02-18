import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- LLM Configuration ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LLM_MODEL = os.getenv("LLM_MODEL", "llama-3.3-70b-versatile")

# --- Embedding Configuration ---
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

# --- Vector Store Configuration ---
VECTOR_STORE_PATH = os.path.join(os.path.dirname(__file__), "vector_store")

# --- Data Configuration ---
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

# --- Chunking Configuration ---
CHUNK_SIZE = 500        
CHUNK_OVERLAP = 50      

# --- Retrieval Configuration ---
TOP_K = 4               
