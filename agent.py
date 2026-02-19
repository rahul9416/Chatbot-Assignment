from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langchain_core.tools import tool
from config import GROQ_API_KEY, LLM_MODEL, VECTOR_STORE_PATH, TOP_K
from tools.pricing_estimator import estimate_price
from embeddings import load_vector_store

@tool
def pricing_tool(project_type: str, duration: str, complexity: str = "medium") -> dict:
    """Estimate the cost of a service. Use this when the user asks about pricing, cost, or budget.
    Available service types: ai_consulting, digital_marketing, web_development, cloud_devops.
    Complexity can be: low, medium, high.

    Args:
        project_type: The type of service. Must be one of: ai_consulting, digital_marketing, web_development, cloud_devops.
        duration: The project duration as a number of months (e.g., "3" for a 3-month project). If the user gives a range like 3-4 months, pick the higher value.
        complexity: Project complexity level. Must be one of: low, medium, high. Default is medium.
    """
    try:
        return estimate_price(project_type, duration, complexity)
    except Exception as e:
        return {"error": f"Pricing estimation failed: {str(e)}"}


def create_custom_agent():
    try:
        llm = ChatGroq(model=LLM_MODEL, api_key=GROQ_API_KEY)
        tools = [pricing_tool]

        system_prompt = (
            "You are a helpful assistant for Techculture, a technology services company. "
            "Use the provided context to answer questions. Always cite sources. "
            "If the user asks about pricing/cost, use the pricing_tool. "
            "If the context doesn't have the answer, say so honestly.\n\n"
            "Context:\n{context}"
        )

        agent = create_agent(llm, tools, system_prompt=system_prompt)
        return agent
    except Exception as e:
        raise RuntimeError(f"Failed to create agent: {str(e)}") from e


def run_agent(query: str) -> str:
    """Run the agent with the given user query and return the response.
    
    Args:
        query: The user's question.
        
    Returns:
        The agent's response as a string.
    """
    try:
        vector_store = load_vector_store(VECTOR_STORE_PATH)
    except Exception as e:
        return f"Error loading vector store: {str(e)}"

    try:
        relevant_chunks = vector_store.similarity_search(query, k=TOP_K)
    except Exception as e:
        return f"Error during similarity search: {str(e)}"

    context = ""
    for chunk in relevant_chunks:
        source = chunk.metadata.get("source", "unknown")
        context += f"[Source: {source}]\n{chunk.page_content}\n\n"

    user_message = f"Context:\n{context}\n\nQuestion: {query}"

    try:
        agent_executor = create_custom_agent()
        result = agent_executor.invoke({"messages": [("user", user_message)]})
        return result["messages"][-1].content
    except Exception as e:
        return f"Error during agent execution: {str(e)}"

