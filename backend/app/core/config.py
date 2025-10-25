from pydantic import BaseSettings, validator

from typing import List

class Settings(BaseSettings):
    """Application settings for LegalEase AI"""

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
    MONGODB_URL: str
    DATABASE_NAME: str

    # AI APIs
    GEMINI_API_KEY: str

    # File Upload
    MAX_FILE_SIZE: int = 10485760  # 10MB
    ALLOWED_FILE_TYPES: List[str] = ["pdf", "docx", "txt", "png", "jpg", "jpeg"]

    # 👇 Fix for parsing env vars correctly (handles CSV input)
    @validator("ALLOWED_FILE_TYPES", pre=True)
    def parse_csv(cls, v):
        if isinstance(v, str):
            # Convert "pdf,docx,txt" → ["pdf", "docx", "txt"]
            return [x.strip() for x in v.split(",")]
        return v

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Instantiate settings
settings = Settings()
