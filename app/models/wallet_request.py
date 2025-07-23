"""Database models for wallet requests."""

from datetime import datetime
from typing import Optional

from sqlalchemy import Column, DateTime, Integer, String, Text, Float
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass


class WalletRequest(Base):
    """Model for storing wallet request information."""
    
    __tablename__ = "wallet_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    address = Column(String(42), nullable=False, index=True)
    balance = Column(Float, nullable=True)
    bandwidth = Column(Float, nullable=True)
    energy = Column(Float, nullable=True)
    request_timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    response_data = Column(Text, nullable=True)
    error_message = Column(Text, nullable=True)
    
    def __repr__(self) -> str:
        """String representation of WalletRequest."""
        return f"<WalletRequest(id={self.id}, address='{self.address}', timestamp='{self.request_timestamp}')>"
