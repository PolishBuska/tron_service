"""Application configuration module."""

import os
from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    app_name: str = "TRON Wallet Service"
    debug: bool = False
    database_url: str = "sqlite:///./data/tron_wallet.db"
    tron_network: str = "mainnet"  # mainnet, shasta, nile
    
    class Config:
        env_file = ".env"


def get_settings() -> Settings:
    """Get application settings instance."""
    return Settings()


settings = get_settings()
