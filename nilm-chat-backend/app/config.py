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
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "flan-t5")  # Updated default to flan-t5
    # OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    # ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    MODEL_NAME: str = os.getenv("MODEL_NAME", "google/flan-t5-large")  # Default to flan-t5-large
    
    # Flan-T5 specific settings
    DEVICE: str = os.getenv("DEVICE", "cpu")  # 'cpu' or 'cuda' for GPU
    MAX_NEW_TOKENS: int = int(os.getenv("MAX_NEW_TOKENS", "512"))
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.7"))
    
    # CORS settings
    CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:5173"]

    class Config:
        env_file = ".env"

settings = Settings()