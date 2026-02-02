"""
config.py - Application Configuration

Purpose:
- Centralized configuration management
- Environment-aware settings
- Production-safe configuration

Usage:
from app.config import settings
print(settings.api_key)
"""

from pydantic_settings import BaseSettings
from typing import Literal
import os


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables
    
    Environment variables override defaults
    """
    
    # ============================================
    # API & Authentication
    # ============================================
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    
    # ============================================
    # Application Environment
    # ============================================
    app_env: Literal["development", "staging", "production"] = os.getenv(
        "APP_ENV", "development"
    )
    debug: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # ============================================
    # Server Configuration
    # ============================================
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8000"))
    
    # ============================================
    # Frontend Configuration
    # ============================================
    frontend_url: str = os.getenv(
        "FRONTEND_URL", "http://localhost:5173"
    )
    
    # ============================================
    # Application Metadata
    # ============================================
    app_name: str = "Smart Video Learning Tool API"
    app_version: str = "0.1.0"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Create settings instance
settings = Settings()

# Validation: Warn if running in production without proper setup
if settings.app_env == "production":
    if not settings.openai_api_key:
        print("⚠️  WARNING: OPENAI_API_KEY not set in production environment!")
    if settings.debug:
        print("⚠️  WARNING: DEBUG=True in production! Set DEBUG=False for security.")
