from embeddings import load_vector_store
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from config import GROQ_API_KEY, LLM_MODEL, VECTOR_STORE_PATH, TOP_K

def retrieve(query, top_k=4):
    """Retrieve relevant document chunks from the vector store."""
    try:
        vectorstore = load_vector_store(VECTOR_STORE_PATH)
        return vectorstore.similarity_search(query, k=top_k)
    except FileNotFoundError:
        raise RuntimeError(f"Vector store not found at '{VECTOR_STORE_PATH}'. Please run the ingestion pipeline first.")
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve documents: {str(e)}") from e


def format_context(chunks):
    """Format retrieved chunks into a context string with source citations."""
    try:
        context_text = ""
        for i, chunk in enumerate(chunks):
            source = chunk.metadata.get("source", "unknown")
            context_text += f"[Source: {source}]\n{chunk.page_content}\n\n"
        return context_text
    except Exception as e:
        raise RuntimeError(f"Failed to format context: {str(e)}") from e


def generate_answer(query, context, tool_output=None):
    """Generate an answer using the LLM with the given context and optional tool output."""
    try:
        prompt = f"Question: {query}\n\nContext:\n{context}"

        if tool_output:
            prompt += f"\n\nTool Output (Pricing Estimate):\n{tool_output}"

        llm = ChatGroq(model=LLM_MODEL, api_key=GROQ_API_KEY)

        system_message = (
            "You are a helpful assistant for Techculture, a technology services company. "
            "Answer questions based ONLY on the provided context. "
            "Always include source citations in your answer (e.g., 'Source: data/ai_consulting.md'). "
            "If tool output (like pricing estimates) is provided, integrate it naturally into your answer. "
            "If the context doesn't contain enough information to answer, say so honestly."
        )

        response = llm.invoke(
            [
                SystemMessage(content=system_message),
                HumanMessage(content=prompt)
            ]
        )
        return response.content
    except Exception as e:
        raise RuntimeError(f"Failed to generate answer: {str(e)}") from e


def ask(query, tool_output=None):
    """Full RAG pipeline: retrieve → format context → generate answer.

    This is the main entry point for the RAG pipeline.
    
    Args:
        query: The user's question.
        tool_output: Optional output from a tool (e.g., pricing estimator)
                     to be integrated into the answer.

    Returns:
        The generated answer as a string.
    """
    try:
        chunks = retrieve(query)
        context = format_context(chunks)
        answer = generate_answer(query, context, tool_output=tool_output)
        return answer
    except RuntimeError:
        raise
    except Exception as e:
        raise RuntimeError(f"RAG pipeline failed: {str(e)}") from e
