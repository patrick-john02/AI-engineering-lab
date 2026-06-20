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
    # qdrant_api_key: str | None = Field(default=None)
    qdrant_collection_name: str = Field(default="api_knowledge_base")
    
    #llm settings
    ollama_base_url: str = Field(default="http://localhost:11434/v1")
    default_model: str = Field(default="qwen2.5:3b")
    
    # openai_api_key: str | None = Field(default=None)
    # gemini_api_key: str | None = Field(default=None)
    
    #logfire settings
    logfire_token: str | None = Field(default=None)
    environment: str = Field(default="development")
    
    
    
env_params = {}
if qdrant_url := os.getenv("QDRANT_URL"):
    env_params["qdrant_url"] = qdrant_url
if qdrant_api_key := os.getenv("QDRANT_API_KEY"):
    env_params["qdrant_api_key"] = qdrant_api_key
if qdrant_collection_name := os.getenv("QDRANT_COLLECTION_NAME"):
    env_params["qdrant_collection_name"] = qdrant_collection_name
if ollama_base_url := os.getenv("OLLAMA_BASE_URL"):
    env_params["ollama_base_url"] = ollama_base_url
if default_model := os.getenv("DEFAULT_MODEL"):
    env_params["default_model"] = default_model
if openai_api_key := os.getenv("OPEN_AI_API_KEY"):
    env_params["openai_api_key"] = openai_api_key
if gemini_api_key := os.getenv("GEMINI_API_KEY"):
    env_params["gemini_api_key"] = gemini_api_key
if logfire_token := os.getenv("LOGFIRE_TOKEN"):
    env_params["logfire_token"] = logfire_token
if environment := os.getenv("ENV"):
    env_params["environment"] = environment

settings = Settings(**env_params)
