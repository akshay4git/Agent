import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    # Application settings
    APP_NAME: str = "NILM Chat API"
    APP_VERSION: str = "0.1.0"
    API_PREFIX: str = "/api"
    
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./nilm_chat.db")
    
    # LLM settings
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "flan-t5")  # Default to flan-t5
    MODEL_NAME: str = os.getenv("MODEL_NAME", "google/flan-t5-large")  # Default to flan-t5-large
    
    # Flan-T5 specific settings
    DEVICE: str = os.getenv("DEVICE", "cpu")  # 'cpu' or 'cuda' for GPU
    MAX_NEW_TOKENS: int = int(os.getenv("MAX_NEW_TOKENS", "512"))
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.7"))
    
    # Conversation history settings
    MAX_CONVERSATION_HISTORY: int = int(os.getenv("MAX_CONVERSATION_HISTORY", "10"))  # Default to 10
    
    # Model cache timeout (in seconds)
    MODEL_CACHE_TIMEOUT: int = int(os.getenv("MODEL_CACHE_TIMEOUT", "3600"))  # Default to 1 hour
    
    # CORS settings
    CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:5173"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()