from ingestion import run_ingestion
from embeddings import create_vector_store, save_vector_store

def initialize():
    """Run the full initialization pipeline: ingest documents → create embeddings → save vector store."""
    print("=" * 50)
    print("  Initializing Service Information Assistant")
    print("=" * 50)

    try:
        chunks = run_ingestion()
    except Exception as e:
        print(f"\n[ERROR] Ingestion failed: {str(e)}")
        return

    try:
        print("\nCreating vector store...")
        vectorstore = create_vector_store(chunks)
    except Exception as e:
        print(f"\n[ERROR] Vector store creation failed: {str(e)}")
        return

    try:
        save_vector_store(vectorstore)
    except Exception as e:
        print(f"\n[ERROR] Failed to save vector store: {str(e)}")
        return

    print("\n" + "=" * 50)
    print(f"  Initialization complete!")
    print(f"  Documents loaded → Chunks created: {len(chunks)}")
    print(f"  Vector store ready for queries.")
    print("=" * 50)


if __name__ == "__main__":
    initialize()
