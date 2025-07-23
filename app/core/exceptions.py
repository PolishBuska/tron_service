"""Custom exceptions module."""

from typing import Any, Dict, Optional
from fastapi import status


class AppException(Exception):
    """Base exception for TRON Wallet Service."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class InvalidAddressException(AppException):
    """Exception raised when TRON address is invalid."""
    pass


class TronNetworkException(AppException):
    """Exception raised when TRON network request fails."""
    pass


class DatabaseException(AppException):
    """Exception raised when database operation fails."""
    pass


class WalletNotFoundException(AppException):
    """Exception raised when wallet is not found."""
    pass


class ValidationException(AppException):
    """Exception raised when data validation fails."""
    pass



EXCEPTION_STATUS_CODE_MAP = {
    "InvalidAddressException": status.HTTP_400_BAD_REQUEST,
    "TronNetworkException": status.HTTP_502_BAD_GATEWAY,
    "DatabaseException": status.HTTP_500_INTERNAL_SERVER_ERROR,
    "WalletNotFoundException": status.HTTP_404_NOT_FOUND,
    "ValidationException": status.HTTP_422_UNPROCESSABLE_ENTITY,
    "AppException": status.HTTP_500_INTERNAL_SERVER_ERROR,
}


TronWalletServiceException = AppException
