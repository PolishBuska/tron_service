"""Global exception handlers for FastAPI application."""

import logging
from typing import Union

from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.exceptions import (
    AppException,
    EXCEPTION_STATUS_CODE_MAP
)

logger = logging.getLogger(__name__)


def create_error_response(
    status_code: int,
    error_type: str,
    message: str,
    details: dict = None
) -> JSONResponse:
    """Create standardized error response."""
    content = {
        "error": {
            "type": error_type,
            "message": message,
            "status_code": status_code
        }
    }
    
    if details:
        content["error"]["details"] = details
    
    return JSONResponse(
        status_code=status_code,
        content=content
    )


async def app_exception_handler(
    request: Request, 
    exc: AppException
) -> JSONResponse:
    """Handle all application exceptions using status code mapping."""
    exception_name = exc.__class__.__name__
    status_code = EXCEPTION_STATUS_CODE_MAP.get(exception_name, status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # Log based on severity
    if status_code >= 500:
        logger.error(f"{exception_name}: {exc.message}")
    elif status_code >= 400:
        logger.warning(f"{exception_name}: {exc.message}")
    else:
        logger.info(f"{exception_name}: {exc.message}")
    
    return create_error_response(
        status_code=status_code,
        error_type=exception_name.replace("Exception", "").upper(),
        message=exc.message,
        details=exc.details
    )


async def validation_exception_handler(
    request: Request, 
    exc: RequestValidationError
) -> JSONResponse:
    """Handle request validation exceptions."""
    logger.warning(f"Validation error: {exc.errors()}")
    return create_error_response(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        error_type="VALIDATION_ERROR",
        message="Request validation failed",
        details={"validation_errors": exc.errors()}
    )


async def http_exception_handler(
    request: Request, 
    exc: StarletteHTTPException
) -> JSONResponse:
    """Handle HTTP exceptions."""
    logger.warning(f"HTTP error {exc.status_code}: {exc.detail}")
    return create_error_response(
        status_code=exc.status_code,
        error_type="HTTP_ERROR",
        message=exc.detail or "HTTP error occurred"
    )


async def general_exception_handler(
    request: Request, 
    exc: Exception
) -> JSONResponse:
    """Handle unexpected exceptions."""
    logger.exception(f"Unexpected error: {str(exc)}")
    return create_error_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        error_type="INTERNAL_ERROR",
        message="An unexpected error occurred"
    )
