from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from config import GROQ_API_KEY, LLM_MODEL
from tools.pricing_estimator import estimate_price
from rag_pipeline import ask

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


def run_agent(query: str) -> str:
    """Agentic orchestrator: the LLM autonomously decides whether to call
    the pricing tool, then the RAG pipeline generates the final answer.

    Flow:
        1. LLM with bound tools sees the query and decides if a tool is needed
        2. If yes → execute the tool → pass tool output to RAG pipeline
        3. If no  → call RAG pipeline directly
        4. RAG pipeline always handles: retrieve → format context → generate answer

    Args:
        query: The user's question.

    Returns:
        The agent's response as a string.
    """
    tool_output = None
    try:
        llm = ChatGroq(model=LLM_MODEL, api_key=GROQ_API_KEY)
        llm_with_tools = llm.bind_tools([pricing_tool])

        response = llm_with_tools.invoke([HumanMessage(content=query)])

        if response.tool_calls:
            tool_call = response.tool_calls[0]
            tool_output = pricing_tool.invoke(tool_call["args"])
    except Exception as e:
        tool_output = {"error": f"Tool decision/execution failed: {str(e)}"}

    try:
        answer = ask(query, tool_output=tool_output)
        return answer
    except Exception as e:
        return f"Error: {str(e)}"
