from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage, AIMessage

from chat_app.agents.supervisor_agent import supervisor_agent
from chat_app.agents.search_agent import search_agent
from chat_app.agents.first_agent import first_agent

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    context: str 

#node 1
async def supervisor_node(state: AgentState):
    user_message = state["messages"][-1].content
    result = await supervisor_agent.run(user_message)
    decision = result.output.strip().lower()
    destination = "search_agent" if "search_agent" in decision else "firt_agent"
    
    return {
        "messages": [AIMessage(content=f"[Supervisor Decision: Route to {destination}]")],
        "context": state.get("context", "")
    }


#node 2
async def search_node(state: AgentState):

    user_message = state["messages"][-2].content
    result = await search_agent.run(user_message)
    
    return {
        "messages": [AIMessage(content="Search Results retrieved successfully.")],
        "context": result.output
    }

#node 3
async def first_agent_node(state: AgentState):
    # Pass search context to standard chatbot agent to finalize the output
    context = state.get("context", "")
    user_message = state["messages"][0].content
    
    prompt = f"Context from database/APIs:\n{context}\n\nUser Question: {user_message}"
    result = await first_agent.run(prompt)
    
    return {
        "messages": [AIMessage(content=result.output)]
    }


#conditional routing based on the supervisor agent decision
def route_next(state: AgentState):
    last_msg = state["messages"][-1].content
    if "Route to search_agent" in last_msg:
        return "search_agent"
    else:
        return "first_agent"

# Build pipeline graph
workflow = StateGraph(AgentState)
workflow.add_node("supervisor", supervisor_node)
workflow.add_node("search_agent", search_node)
workflow.add_node("first_agent", first_agent_node)

workflow.add_edge(START, "supervisor")
workflow.add_conditional_edges(
    "supervisor",
    route_next,
    {
        "search_agent": "search_agent",
        "first_agent": "first_agent"
    }
)
workflow.add_edge("search_agent", "first_agent")
workflow.add_edge("first_agent", END)

memory = MemorySaver()
graph = workflow.compile(checkpointer=memory)
