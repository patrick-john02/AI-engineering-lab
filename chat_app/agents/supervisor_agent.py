from pydantic_ai import Agent
from pydantic_ai.models.ollama import OllamaModel
from pydantic_ai.providers.ollama import OllamaProvider
from chat_app.config import settings
from pydantic import BaseModel
from typing import Literal

model = OllamaModel(
    settings.default_model,
    provider=OllamaProvider(
        base_url=settings.ollama_base_url,
    ),
)

class RouterDecision(BaseModel):
    destination: Literal["search_agent", "first_agent"]
    reasoning: str

supervisor_agent = Agent(
    model,
    # output_type=RouterDecision,
    system_prompt=(
        "You are an AI supervisor routing user queries in a RAG system.\n"
        "Your task is to analyze the user query and decide which agent should handle it:\n"
        "1. Route to 'search_agent' if the query asks to retrieve real-time data, search users, todos, posts, or query the knowledge base.\n"
        "2. Route to 'first_agent' if the query is a general question, greeting, or request that does not require database/API search."
    )
)
