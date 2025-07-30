"""Application settings"""
from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # Application
    app_name: str = "KBI Labs Intelligence Platform"
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    port: int = int(os.getenv("PORT", "8000"))
    
    # Security
    secret_key: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # CORS
    allowed_origins: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://3.143.232.123:8000"
    ]
    
    # Database
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./kbi_labs.db")
    
    # Redis
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # External APIs
    sam_gov_api_key: str = os.getenv("SAM_GOV_API_KEY", "")
    uspto_api_key: str = os.getenv("USPTO_API_KEY", "")
    
    class Config:
        env_file = ".env"

settings = Settings()

def get_settings():
    return settings
