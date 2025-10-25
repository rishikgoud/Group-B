"""
Core configuration settings for LegalEase AI
"""

from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "LegalEase AI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    PROJECT_NAME: str = "LegalEase AI Contract Analyzer"
    
    # API
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ]
    
    # Database
    DATABASE_URL: str = "sqlite:///./data/legalease.db"
    
    # AI APIs
    GEMINI_API_KEY: str = ""
    PERPLEXITY_API_KEY: str = ""
    
    # File Upload
    MAX_FILE_SIZE: int = 10485760  # 10MB
    ALLOWED_FILE_TYPES: List[str] = ["pdf", "docx", "txt", "png", "jpg", "jpeg"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create settings instance
settings = Settings()
