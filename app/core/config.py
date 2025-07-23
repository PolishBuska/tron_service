"""Application configuration module."""

import os
from typing import Optional

from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    """Application settings."""
    
    model_config = ConfigDict(env_file=".env")
    
    app_name: str = "TRON Wallet Service"
    debug: bool = False
    database_url: str = "sqlite:///./data/tron_wallet.db"
    tron_network: str = "mainnet"  # mainnet, shasta, nile


def get_settings() -> Settings:
    """Get application settings instance."""
    return Settings()


settings = get_settings()
