from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import DATA_DIR, CHUNK_OVERLAP, CHUNK_SIZE

def load_documents():
    loader = DirectoryLoader(DATA_DIR, glob="**/*.md", loader_cls=TextLoader, loader_kwargs={"encoding": "utf-8"})
    return loader.load()

def chunk_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ".", " "]
    )
    return text_splitter.split_documents(documents)

def run_ingestion():
    print("loading documents")
    documents = load_documents()
    print(f"loaded {len(documents)} documents")
    print("chunking documents")
    chunks = chunk_documents(documents)
    print(f"chunked {len(chunks)} documents")
    return chunks

# if __name__ == "__main__":
#     chunks = run_ingestion()