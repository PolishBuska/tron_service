"""Database models for wallet requests."""

from datetime import datetime
from typing import Optional

from sqlalchemy import String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass


class WalletRequest(Base):
    """Model for storing wallet request information."""
    
    __tablename__ = "wallet_requests"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    address: Mapped[str] = mapped_column(String(42), nullable=False, index=True)
    balance: Mapped[Optional[float]] = mapped_column(nullable=True)
    bandwidth: Mapped[Optional[float]] = mapped_column(nullable=True)
    energy: Mapped[Optional[float]] = mapped_column(nullable=True)
    request_timestamp: Mapped[datetime] = mapped_column(
        nullable=False, 
        index=True,
        server_default=func.now()
    )
    response_data: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    def __repr__(self) -> str:
        """String representation of WalletRequest."""
        return f"<WalletRequest(id={self.id}, address='{self.address}', timestamp='{self.request_timestamp}')>"
