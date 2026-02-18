from embeddings import load_vector_store
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from config import GROQ_API_KEY, LLM_MODEL, VECTOR_STORE_PATH, TOP_K

def retrieve(query, top_k=4):
    vectorstore = load_vector_store(VECTOR_STORE_PATH)
    return vectorstore.similarity_search(query, k=top_k)

def format_context(chunks):
    context_text = ""
    for i, chunk in enumerate(chunks):
        source = chunk.metadata.get("source", "unknown")
        context_text += f"[Source: {source}]\n{chunk.page_content}\n\n"
    return context_text

def generate_answer(query, context):
    prompt = f"""Answer the question based on the context provided.

    Context: {context}

    Question: {query}

    Answer: """

    llm = ChatGroq(model=LLM_MODEL, api_key=GROQ_API_KEY)
    response = llm.invoke(
        [
            SystemMessage(content="You are a helpful assistant for Techculture, a technology services company. Answer questions based ONLY on the provided context. Always include source citations in your answer (e.g., 'Source: data/ai_consulting.md'). If the context doesn't contain enough information to answer, say so honestly."),
            HumanMessage(content=prompt)
        ]
    )
    return response.content

def ask(query):
    chunks = retrieve(query)
    context = format_context(chunks)
    answer = generate_answer(query, context)
    return answer


if __name__ == "__main__":
    print("RAG pipeline")
    query = "What AI services do you offer?"
    results = ask(query)
    print(results)