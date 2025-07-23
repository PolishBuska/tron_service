"""Pydantic schemas for wallet-related API operations."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, validator


class WalletAddressRequest(BaseModel):
    """Schema for wallet address request."""
    
    address: str = Field(..., description="TRON wallet address")
    
    @validator('address')
    def validate_address(cls, v: str) -> str:
        """Validate TRON address format."""
        if not v or len(v) != 42 or not v.startswith('T'):
            raise ValueError('Invalid TRON address format')
        return v


class WalletInfoResponse(BaseModel):
    """Schema for wallet information response."""
    
    address: str = Field(..., description="TRON wallet address")
    balance: Optional[float] = Field(None, description="TRX balance in TRX units")
    bandwidth: Optional[float] = Field(None, description="Available bandwidth")
    energy: Optional[float] = Field(None, description="Available energy")
    
    class Config:
        from_attributes = True


class WalletRequestRecord(BaseModel):
    """Schema for wallet request record."""
    
    id: int = Field(..., description="Record ID")
    address: str = Field(..., description="TRON wallet address")
    balance: Optional[float] = Field(None, description="TRX balance")
    bandwidth: Optional[float] = Field(None, description="Available bandwidth")
    energy: Optional[float] = Field(None, description="Available energy")
    request_timestamp: datetime = Field(..., description="Request timestamp")
    error_message: Optional[str] = Field(None, description="Error message if any")
    
    class Config:
        from_attributes = True


class WalletRequestsResponse(BaseModel):
    """Schema for paginated wallet requests response."""
    
    records: List[WalletRequestRecord] = Field(..., description="List of wallet request records")
    total: int = Field(..., description="Total number of records")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Page size")
    total_pages: int = Field(..., description="Total number of pages")


class PaginationParams(BaseModel):
    """Schema for pagination parameters."""
    
    page: int = Field(1, ge=1, description="Page number")
    page_size: int = Field(10, ge=1, le=100, description="Page size")
