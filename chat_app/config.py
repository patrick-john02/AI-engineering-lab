import os
from pathlib import Path
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseModel):
    project_name: str = "Agentic RAG Engineering Lab"
    version: str = "1.0"
    base_dir: Path = Path(__file__).resolve().parent.parent
    
    #Qdrant settings
    qdrant_url: str = Field(default="http://localhost:6333/")
    qdrant_api_key = str | None - Field(default=None)
    qdrant_collection_name: str = Field(default="api_knowledge_base")
    
    #llm settings
    ollama_base_url: str = Field(default="http://localhost:11434/v1")
    default_model: str = Field(default="qwen2.5:3b")
    openai_api_key: str | None = Field(default=None)
    gemini_api_key: str | None = Field(default=None)
    
    #logfire settings
    logfire_token: str | None = Field(default=None)
    environment: str = Field(default="development")
    
    
    
settings = Settings(
    qdrant_url=os.getenv("QDRANT_URL", "http://localhost:6333"),
    qdrant_api_key=os.getenv("QDRANT_API_KEY"),
    qdrant_collection_name=os.getenv("QDRANT_COLLECTION_NAME"),
    ollama_base_url=os.getenv("OLLAMA_BASE_URL"),
    default_model=os.getenv("DEFAULT_MODEL", "qwen2.5:3b"),
    open_api_key=os.getenv("OPEN_AI_API_KEY"),
    gemini_api_key=os.getenv("GEMINI_API_KEY"),
    logfire=os.getenv("LOGFIRE_TOKEN"),
    environment=os.getenv("ENV", "development"),
)
