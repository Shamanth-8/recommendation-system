from pydantic import BaseSettings, Field
from typing import List
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "Assessment Recommendation Engine"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "your-secret-key-here"  # Change this in production
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # YouTube Data API
    YOUTUBE_API_KEY: str = os.getenv("YOUTUBE_API_KEY")
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
