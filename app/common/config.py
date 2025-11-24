"""
Common configuration module for the ad-campaign agent system.
Loads environment variables and provides centralized configuration.
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Service URLs
    PRODUCT_SERVICE_URL: str = "http://localhost:8001"
    CREATIVE_SERVICE_URL: str = "http://localhost:8002"
    STRATEGY_SERVICE_URL: str = "http://localhost:8003"
    META_SERVICE_URL: str = "http://localhost:8004"
    LOGS_SERVICE_URL: str = "http://localhost:8005"
    SCHEMA_VALIDATOR_SERVICE_URL: str = "http://localhost:8006"
    OPTIMIZER_SERVICE_URL: str = "http://localhost:8007"
    
    # Orchestrator settings
    GEMINI_API_KEY: Optional[str] = None
    GEMINI_MODEL: str = "gemini-2.0-flash-exp"
    
    # General settings
    LOG_LEVEL: str = "INFO"
    ENVIRONMENT: str = "development"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()
