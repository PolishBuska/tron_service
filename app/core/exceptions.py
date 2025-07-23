"""Custom exceptions module."""

from typing import Any, Dict, Optional


class TronWalletServiceException(Exception):
    """Base exception for TRON Wallet Service."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class InvalidAddressException(TronWalletServiceException):
    """Exception raised when TRON address is invalid."""
    pass


class TronNetworkException(TronWalletServiceException):
    """Exception raised when TRON network request fails."""
    pass


class DatabaseException(TronWalletServiceException):
    """Exception raised when database operation fails."""
    pass


class WalletNotFoundException(TronWalletServiceException):
    """Exception raised when wallet is not found."""
    pass
