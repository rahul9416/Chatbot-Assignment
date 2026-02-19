from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import DATA_DIR, CHUNK_OVERLAP, CHUNK_SIZE

def load_documents():
    """Load all markdown documents from the data directory."""
    try:
        loader = DirectoryLoader(DATA_DIR, glob="**/*.md", loader_cls=TextLoader, loader_kwargs={"encoding": "utf-8"})
        return loader.load()
    except Exception as e:
        raise RuntimeError(f"Failed to load documents from '{DATA_DIR}': {str(e)}") from e

def chunk_documents(documents):
    """Split documents into smaller chunks for embedding."""
    try:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            separators=["\n\n", "\n", ".", " "]
        )
        return text_splitter.split_documents(documents)
    except Exception as e:
        raise RuntimeError(f"Failed to chunk documents: {str(e)}") from e

def run_ingestion():
    """Full ingestion pipeline: load documents → chunk them."""
    try:
        print("Loading documents...")
        documents = load_documents()
        print(f"Loaded {len(documents)} documents")
        print("Chunking documents...")
        chunks = chunk_documents(documents)
        print(f"Created {len(chunks)} chunks")
        return chunks
    except Exception as e:
        raise RuntimeError(f"Ingestion failed: {str(e)}") from e