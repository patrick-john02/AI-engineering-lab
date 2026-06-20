from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
import logfire
from dotenv import load_dotenv
from chat_app.agents.first_agent import first_agent
from chat_app.tools.client import close_client
from chat_app.graph import graph

load_dotenv()
logfire.configure()

@asynccontextmanager
async def lifespan(app: FastAPI):

    # instrument FastAPI with logfire
    logfire.instrument_fastapi(app)
    yield

    await close_client()

# Initialize the FastAPI application with metadata
app = FastAPI(
    title="RAG Engineering Lab",
    description="Chat bot using different public endpoints.",
    version="1.0.0",
    lifespan=lifespan
)

class ChatRequest(BaseModel):
    prompt: str
    session_id: str = "default_session"

class ChatResponse(BaseModel):
    response: str

@app.get('/')
async def root():

    return {"status": "ok", "message": "Chatbot service is operational"}

@app.post('/chat', response_model=ChatResponse)
async def chat(request: ChatRequest):
    

    try:
        # result = await first_agent.run(request.prompt)
        # return ChatResponse(response=result.data)
        
        initial_state = {
            "messages" : [HumanMessage(content=request.prompt)],
            "context": ""
        }
        
        config = {"configurable": {"thread_id": request.session_id}}
        final_state = await graph.ainvoke(initial_state, config=config)
        
        
        final_response = final_state["messages"][-1].content
        return ChatResponse(response=final_response)
    
    
    except Exception as e:
        logfire.error(f"Chat request failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error occurred while processing your request.")
