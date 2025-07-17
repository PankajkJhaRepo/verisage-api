"""
Configuration settings for Verisage API
"""
try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseSettings
from typing import List

class Settings(BaseSettings):
                       
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    
    ALLOWED_ORIGINS: List[str] = ["*"]                                         
    
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Verisage API"
    
    OPENAI_API_KEY: str = ""
    OPENAI_API_BASE: str = ""
    LLM_MODEL: str = "gpt-4o"
    EMBEDDINGS_MODEL: str = "text-embedding-3-large"
    
    TAVILY_API_KEY: str = ""
    
    STORE_BATCH_SIZE: int = 100
    TEXTSPLITTER_CHUNK_SIZE: int = 600
    TEXTSPLITTER_CHUNK_OVERLAP: int = 100
    
    PGVECTOR_CONNECTION: str = ""
    PGVECTOR_COLLECTION_NAME: str = "storage_4_langgraph"
    
    LANGSMITH_TRACING: bool = True
    LANGSMITH_TRACING_V2: bool = True
    LANGSMITH_ENDPOINT: str = "https://api.smith.langchain.com"
    LANGSMITH_API_KEY: str = ""
    LANGSMITH_PROJECT: str = "pr-abandoned-model-68"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
