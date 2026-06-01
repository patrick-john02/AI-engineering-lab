from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from pydantic import BaseModel
import logfire
from dotenv import load_dotenv
from chat_app.agents.first_agent import first_agent
from chat_app.tools.client import close_client

# Industry standard: Centralize configuration at the application entry point
load_dotenv()
logfire.configure()

@asynccontextmanager
async def lifespan(app: FastAPI):

    # Correctly instrument FastAPI with logfire
    logfire.instrument_fastapi(app)
    yield
    # Clean up resources on shutdown
    await close_client()

# Initialize the FastAPI application with metadata
app = FastAPI(
    title="RAG Engineering Lab",
    description="An industry-standard chatbot integration using Pydantic AI and FastAPI.",
    version="1.0.0",
    lifespan=lifespan
)

class ChatRequest(BaseModel):
    prompt: str

class ChatResponse(BaseModel):
    response: str

@app.get('/')
async def root():

    return {"status": "ok", "message": "Chatbot service is operational"}

@app.post('/chat', response_model=ChatResponse)
async def chat(request: ChatRequest):

    try:
        # Execute the agent synchronously for the simple REST endpoint
        # For long-running tasks, consider using the streaming interface
        result = await first_agent.run(request.prompt)
        return ChatResponse(response=result.data)
    except Exception as e:
        logfire.error(f"Chat request failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error occurred while processing your request.")
