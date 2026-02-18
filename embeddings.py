from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from config import EMBEDDING_MODEL, VECTOR_STORE_PATH
from ingestion import run_ingestion

def get_embedding_model():
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

def create_vector_store(chunks):
    embeddings = get_embedding_model()
    vectorstore = FAISS.from_documents(chunks, embeddings)
    return vectorstore

def save_vector_store(vectorstore):
    vectorstore.save_local(VECTOR_STORE_PATH)
    print("Vector store saved to disk")

def load_vector_store(path):
    embeddings = get_embedding_model()
    return FAISS.load_local(path, embeddings, allow_dangerous_deserialization=True)


if __name__ == "__main__":
    chunks = run_ingestion()
    vectorstore = create_vector_store(chunks)
    save_vector_store(vectorstore)

