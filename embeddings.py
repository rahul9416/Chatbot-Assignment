from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from config import EMBEDDING_MODEL, VECTOR_STORE_PATH

def get_embedding_model():
    """Load the HuggingFace embedding model."""
    try:
        return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    except Exception as e:
        raise RuntimeError(f"Failed to load embedding model '{EMBEDDING_MODEL}': {str(e)}") from e

def create_vector_store(chunks):
    """Create a FAISS vector store from document chunks."""
    try:
        embeddings = get_embedding_model()
        vectorstore = FAISS.from_documents(chunks, embeddings)
        return vectorstore
    except Exception as e:
        raise RuntimeError(f"Failed to create vector store: {str(e)}") from e

def save_vector_store(vectorstore):
    """Save the FAISS vector store to disk."""
    try:
        vectorstore.save_local(VECTOR_STORE_PATH)
        print(f"Vector store saved to '{VECTOR_STORE_PATH}'")
    except Exception as e:
        raise RuntimeError(f"Failed to save vector store: {str(e)}") from e

def load_vector_store(path):
    """Load a persisted FAISS vector store from disk."""
    try:
        embeddings = get_embedding_model()
        return FAISS.load_local(path, embeddings, allow_dangerous_deserialization=True)
    except Exception as e:
        raise RuntimeError(f"Failed to load vector store from '{path}': {str(e)}") from e
