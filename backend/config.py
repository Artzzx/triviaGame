import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables. 
    """
    # API Endpoints
    TRIVIA_API: str
    TRIVIA_TOKEN_API: str
    TRIVIA_CATEGORY_API: str
    
    # Server Configuration
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8000
    DEBUG: bool = False
    
    # Database Configuration
    DATABASE_URL: str
    
    # WebSocket Configuration
    WEBSOCKET_PING_INTERVAL: int = 25
    WEBSOCKET_PING_TIMEOUT: int = 120
    
    # Game Configuration
    DEFAULT_QUESTION_TIME: int = 15
    MAX_PLAYERS_PER_ROOM: int = 8
    QUESTION_CACHE_TTL: int = 86400
    
    # Security
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create a global settings object
settings = Settings()

def get_settings() -> Settings:
    """
    Returns the settings object. 
    """
    return settings