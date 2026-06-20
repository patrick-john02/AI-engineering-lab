from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage, AIMessage

from chat_app.agents.supervisor_agent import supervisor_agent
from chat_app.agents.search_agent import search_agent
from chat_app.agents.first_agent import first_agent

from pydantic_ai.messages import ModelMessage, ModelRequest, UserPromptPart, ModelResponse, TextPart

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    context: str 
    

#this will convert langgraph message into pydantic ai messages
def getpydantic_ai_history(state:AgentState)->list[ModelMessage]:
    history = []
    message_to_convert = state["messages"][:-1]
    for msg in message_to_convert:
        if isinstance(msg, HumanMessage):
            history.append(ModelRequest(parts=[UserPromptPart(content=msg.content)]))
        elif isinstance(msg, AIMessage):
            if msg.content.startswith("[Supervisor Decision:") or msg.content == "search result retrieved sucessfully":
                continue
            history.append(ModelResponse(parts=[TextPart(content=msg.content)]))
    return history 
    

#node 1
async def supervisor_node(state: AgentState):
    # user_message = state["messages"][-1].content
    user_messages = [msg for msg in state["messages"] if isinstance(msg, HumanMessage)]
    user_message = user_messages[-1].content if user_messages else ""
    
    history = getpydantic_ai_history(state)
    result = await supervisor_agent.run(user_message, message_history=history)
    decision = result.output.strip().lower()
    # destination = "search_agent" if "search_agent" in decision else "first_agent"
    destination = "search_agent" if "search" in decision else "first_agent"
    
    return {
        "messages": [AIMessage(content=f"[Supervisor Decision: Route to {destination}]")],
        "context": state.get("context", "")
    }


#node 2
async def search_node(state: AgentState):

    # user_message = state["messages"][-2].content
    user_messages = [msg for msg in state["messages"] if isinstance(msg, HumanMessage)]
    user_message = user_messages[-1].content if user_messages else ""
    
    history = getpydantic_ai_history(state)
    result = await search_agent.run(user_message, message_history=history)
    
    return {
        "messages": [AIMessage(content="Search Results retrieved successfully.")],
        "context": result.output
    }

#node 3
async def first_agent_node(state: AgentState):
    # Pass search context to standard chatbot agent to finalize the output
    context = state.get("context", "")
    # user_message = state["messages"][0].content
    
    user_messages = [msg for msg in state["messages"] if isinstance(msg, HumanMessage)]
    user_message = user_messages[-1].content if user_messages else ""
    
    prompt = f"Context from database/APIs:\n{context}\n\nUser Question: {user_message}"
    
    history = getpydantic_ai_history(state)
    result = await first_agent.run(prompt, message_history=history)
    
    
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
