from pydantic_ai.models.ollama import OllamaModel
from pydantic_ai.providers.ollama import OllamaProvider
from pydantic_ai import Agent


# Configuration is now handled in the main entry point to follow the singleton pattern
model = OllamaModel(
    'qwen2.5:3b',
    provider=OllamaProvider(
        base_url='http://localhost:11434/v1',
    ),
)

#this agent will be a pure generator
first_agent = Agent(
    model,
    system_prompt=(
        "Introduce yourself if the user ask it"
        "You are a ChatBot assistant for users. "
        "Your task is to generate summaries or responses based ONLY on the provided Context from database/APIs."
        
        "GUIDELINES:\n"
        "1. Formulate your response using only facts present in the Context.\n"
        "2. If the Context is empty or states no records were found, "
        "3. NEVER invent data. NEVER type JSON. NEVER explain your process.\n"
        "4. Provide a clear, natural language summary."
    )
)